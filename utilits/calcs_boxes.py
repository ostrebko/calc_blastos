import numpy as np

import os 
os.environ['TP_CPP_MIN_LOG_LEVEL']='2'

import sys
if not sys.warnoptions:
    import warnings
    warnings.simplefilter('ignore')

import glob 
import time
import shutil
import csv

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from PIL import Image
import cv2

from yolov5.segment import predict


class BoxesOneImgNums():
    """
    Decription ...
    
    Args:
    -------------
    config (_dict_) - словарь с конфигурацией
    ...
    """
    
    
    def __init__(self, img_path, model_yolov5, config: dict):
        
        super().__init__()
        
        self.img_path = img_path
        self.img_name = os.path.basename(self.img_path)
        self.folder_name = os.path.basename(os.path.dirname(self.img_path))

        self.model_yolov5 = model_yolov5
        self.config = config
        self.mask_grid = None

        if self.config.type_clc=='in_grid':
            self.mask_grid = self.get_grid_mask()
            self.boxes = self.get_boxes()
            self.num_boxes = self.calc_boxes_with_grid()
        elif self.config.type_clc=='simple':
            self.boxes = self.get_boxes()
            self.num_boxes = self.simple_calc_boxes()
    

    def get_grid_mask(self):
        
        path_to_weights_segm = os.path.join(self.config.path_to_model, self.config.model_segm_name)
        
        predict.run(weights=path_to_weights_segm, 
                    source=self.img_path, 
                    save_txt=True,
                    project=self.config.path_to_predicted_images,                                         
                    name=self.folder_name,
                    exist_ok=True)
        
        img_h, img_w = cv2.imread(self.img_path).shape[:2]
        #img_w, img_h = Image.open(self.img_path).size

        with open(os.path.join(self.config.path_to_predicted_images, 
                               self.folder_name, 'labels', self.img_name)[:-4]+'.txt', "r") as f:
                txt_file = f.readlines()[0].split()
                coords = txt_file[1:]
                polygon = np.array([[eval(x), eval(y)] for x, y in zip(coords[0::2], coords[1::2])])
                polygon[:,0] = (polygon[:,0]/img_w)*self.config.img_size
                polygon[:,1] = (polygon[:,1]/img_h)*self.config.img_size
                polygon = polygon.astype(int)

        mask = np.zeros((self.config.img_size, self.config.img_size)) # , dtype=np.uint8
        mask_grid = np.where(cv2.fillPoly(mask, pts=[polygon], color=(255, 255, 255))>0, 1, 0)
        
        return mask_grid


    
    def get_boxes(self):

        original_image = Image.open(self.img_path)
        max_size = (self.config.img_size, self.config.img_size)
        resized_image = original_image.resize(max_size, Image.ANTIALIAS)
        
        confidece_mask = self.model_yolov5(resized_image, 
                                           size=self.config.img_size).xyxy[0][:,4]>=self.config.bbox_conf #
        boxes = self.model_yolov5(resized_image, size=self.config.img_size).xyxy[0][:, :4]
        boxes = boxes[np.array(confidece_mask)] #
               
        if self.config.is_draw:
            plt.rcParams["figure.figsize"] = (12,8)
            fig, ax = plt.subplots()
            
            if self.config.type_clc=='simple':
                # to save boxes without mask
                plt.imshow(resized_image)
            elif self.config.type_clc=='in_grid':
                # to save boxes with mask
                masked_original_image = Image.open(
                    os.path.join(self.config.path_to_predicted_images, self.folder_name, self.img_name))
                max_size = (self.config.img_size, self.config.img_size)
                masked_resized_image = masked_original_image.resize(max_size, Image.ANTIALIAS)
                
                plt.imshow(masked_resized_image)

            
            for item in boxes:
                width_img = int(item[2] - item[0])
                height_img = int(item[3] - item[1])
                ax = plt.gca()
                rect = patches.Rectangle((item[0],
                                        item[1]), 
                                        width_img, 
                                        height_img, 
                                        linewidth=1, 
                                        edgecolor='red', 
                                        fill = False)
                ax.add_patch(rect)
            
            if not os.path.isdir(os.path.join(self.config.path_to_predicted_images, self.folder_name)):
                os.mkdir(os.path.join(self.config.path_to_predicted_images, self.folder_name))
            
            name_save_file = os.path.join(self.config.path_to_predicted_images, 
                                     self.folder_name, self.img_name[:-4])+ '_boxes.jpg'
            
            plt.savefig(name_save_file, bbox_inches='tight', dpi=300)
            plt.close(fig)

            if not os.path.isdir(os.path.join(self.config.path_to_predicted_images, self.folder_name, 'labels')):
                os.mkdir(os.path.join(self.config.path_to_predicted_images, self.folder_name, 'labels'))

            np.savetxt(os.path.join(self.config.path_to_predicted_images, 
                                    self.folder_name, 'labels', self.img_name[:-4]) + '_boxes.txt', boxes)
        return boxes


    def calc_boxes_with_grid(self):
        
        num_blasto = 0
        for item in self.boxes:
            
            # center bbox in mask
            #if self.mask_grid[int((item[0]+item[2])/2), int((item[1]+item[3])/2)]==1: 
            
            # all coord bbox in mask
            if (self.mask_grid[int(item[0]-1), int(item[1]-1)]==1)&(self.mask_grid[int(item[2]-1), int(item[3]-1)]==1): 
                num_blasto += 1
        
        print(f'название: {self.img_name} число бластоспор в сетке {num_blasto}')

        return num_blasto



    def simple_calc_boxes(self):
        
        num_blasto = int(len(self.boxes)*0.43)
        print(f'название: {self.img_name} оценочное число бластоспор {num_blasto}')

        return num_blasto



class BoxesAvgNums():
    
    """
    Decription ...  
    Args:
    -------------
    config (_dict_) - словарь с конфигурацией
    ...
    """
    
    def __init__(self, folder_name, model_yolov5, config: dict):
        super().__init__()
        self.config = config
        self.calc_avg_num_blastos(folder_name=folder_name, model=model_yolov5)
    

    def calc_avg_num_blastos(self, folder_name, model):
        
        start_time = time.time()

        imgs_paths = sorted(
            glob.glob(os.path.join(self.config.path_to_images, folder_name, '*.jpg')), key=str)
        numb_images = len(imgs_paths)
        
        list_to_calc_avg = []      
        with open(os.path.join(
            self.config.path_to_predicted_images, folder_name, 'result_' + str(folder_name) + '.csv'), 
            'w', newline='') as csvfile:
            for num, imge in enumerate(imgs_paths, start=1):
                print(num, imge)              
                #num_blastos = self.calc_boxes(imge, folder_name, model, is_draw)
                num_blastos = BoxesOneImgNums(imge, model, self.config).num_boxes
                print(f'Фото №{num}/{numb_images},', end=' ') 
                list_to_calc_avg.append(num_blastos)
                csv_writer = csv.writer(csvfile, delimiter=';')
                csv_writer.writerow(list([os.path.basename(imge), num_blastos, ]))
                                        #int(num_blastos*0.43)]))  
            mean_numb_blasto = int(np.mean(list_to_calc_avg))
            print()
            print(f'Среднее число бластоспор: {mean_numb_blasto}')
            csv_writer.writerow(list(['avrg numb', mean_numb_blasto, ]))
                                    #int(mean_numb_blasto*0.43)]))
        print('Время расчета: %s seconds' % (time.time() - start_time), end='\n\n')
        #return