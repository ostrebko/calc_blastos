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

#import torch
from PIL import Image


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
        self.model_yolov5 = model_yolov5
        self.config = config

        self.boxes = self.get_boxes()
        self.num_boxes = self.simple_calc_boxes()
    
    
    def get_boxes(self):
        
        """Для каждой фото рассчитывается количество бластоспор 
        (предсказание запускается на каждое фото). 
        Далее предсказанное количество бластоспор собраются в лист 
        и их число усредняется."""
            
        img_name = os.path.basename(self.img_path)
        folder_name = os.path.basename(os.path.dirname(self.img_path))
        
        original_image = Image.open(self.img_path)
        max_size = (self.config.img_size, self.config.img_size)
        resized_image = original_image.resize(max_size, Image.ANTIALIAS)
        
        boxes = self.model_yolov5(resized_image, size=self.config.img_size).xyxy[0][:, :4]
                
        if self.config.is_draw:
            plt.rcParams["figure.figsize"] = (12,8)
            fig, ax = plt.subplots()
            
            plt.imshow(resized_image)
            
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
            
            if not os.path.isdir(os.path.join(self.config.path_to_predicted_images, folder_name)):
                os.mkdir(os.path.join(self.config.path_to_predicted_images, folder_name))
            save_file = os.path.join(self.config.path_to_predicted_images, folder_name, img_name)
            plt.savefig(save_file, bbox_inches='tight', dpi=300)
            plt.close(fig)

            np.savetxt(os.path.join(self.config.path_to_predicted_images, 
                                    folder_name, img_name[:-4]) + '_boxes.txt', boxes)

        return boxes



    def simple_calc_boxes(self):
        
        img_name = os.path.basename(self.img_path)
        numb_blasto = len(self.boxes)
        print(f'название: {img_name} число бластоспор: {numb_blasto}, оценка в сетке {int(numb_blasto*0.43)}')

        return numb_blasto


    # def calc_boxes_in_grid(self, img_path, model_yolov5, config):
        
    #     """Для каждой фото рассчитывается количество бластоспор в границах сетки
    #     (предсказание запускается на каждое фото). 
    #     Далее предсказанное количество бластоспор собраются в лист 
    #     и их число усредняется."""
            
    #     img_name = os.path.basename(img_path)
    #     folder_name = os.path.basename(os.path.dirname(img_path))
        
    #     original_image = Image.open(img_path)
    #     max_size = (config.img_size, config.img_size)
    #     resized_image = original_image.resize(max_size, Image.ANTIALIAS)
        
    #     boxes = np.array(model_yolov5(resized_image, size=config.img_size).xyxy[0][:, :6])
        
    #     sorted_boxes_cls = boxes[boxes[:,-1].argsort()]
        
    #     num_bboxes_in_grid = 0

    #     if sorted_boxes_cls[0][-1]==0:
    #         zero_class = sorted_boxes_cls[0]
            
    #         left_limit_grid = zero_class[0]
    #         right_limit_grid = zero_class[2]
    #         up_limit_grid = zero_class[1]
    #         down_limit_grid = zero_class[3]
        
    #         for bbox in sorted_boxes_cls[1:]:
    #             x_c = (bbox[2]+bbox[0])/2
    #             y_c = (bbox[3]+bbox[1])/2
    #             if (left_limit_grid <= x_c <= right_limit_grid)and(up_limit_grid <= y_c <= down_limit_grid):
    #                 num_bboxes_in_grid += 1
        
    #     else:
    #         print('сетка не определена')        


    #     print(f'название: {img_name} число бластоспор в сетке: {num_bboxes_in_grid}')
        

    #     if config.is_draw:
    #         plt.rcParams["figure.figsize"] = (12,8)
    #         fig, ax = plt.subplots()
            
    #         plt.imshow(resized_image)
            
    #         for item in boxes:
    #             width_img = int(item[2] - item[0])
    #             height_img = int(item[3] - item[1])
    #             ax = plt.gca()
    #             rect = patches.Rectangle((item[0],
    #                                     item[1]), 
    #                                     width_img, 
    #                                     height_img, 
    #                                     linewidth=1, 
    #                                     edgecolor='red', 
    #                                     fill = False)
    #             ax.add_patch(rect)
            
    #         if not os.path.isdir(os.path.join(config.path_to_predicted_images, folder_name)):
    #             os.mkdir(os.path.join(config.path_to_predicted_images, folder_name))
    #         save_file = os.path.join(config.path_to_predicted_images, folder_name, img_name)
    #         plt.savefig(save_file, bbox_inches='tight', dpi=300)
    #         plt.close(fig) 
            
            
    #     return num_bboxes_in_grid



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
                csv_writer.writerow(list([os.path.basename(imge), num_blastos, 
                                        int(num_blastos*0.43)]))  
            mean_numb_blasto = int(np.mean(list_to_calc_avg))
            print()
            print(f'Среднее число бластоспор: {mean_numb_blasto}')
            csv_writer.writerow(list(['avrg numb', mean_numb_blasto, 
                                    int(mean_numb_blasto*0.43)]))
        print('Время расчета: %s seconds' % (time.time() - start_time))
        #return


#     for fold_name in os.listdir(path_to_images):
#         if os.path.isdir(os.path.join(path_to_predicted_images, fold_name)):
#             shutil.rmtree(os.path.join(path_to_predicted_images, fold_name))
#         os.mkdir(os.path.join(path_to_predicted_images, fold_name))
#         calc_avg_num_blastos(path_to_images, fold_name, model, is_draw=True)

#     print('Well done!!!')
