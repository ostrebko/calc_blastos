#import os
#from utilits.functions import config_reader
#from utilits.model_loader import LoadModel
#from utilits.calcs_boxes import BoxesNums, BoxesAvgNums

from utilits.functions import calc_avg_num_blastos

path_to_config = 'config/data_config.json'
calc_avg_num_blastos(path_to_config)

#config = config_reader(path_to_config)

#model = LoadModel(config).loaded_model

#pathe = 'C:/Users/jaffa/Projects/calc_blastos/image_folder/1/1.jpg'
#print(BoxesNums(pathe, model, config).num_boxes)

#folder_name = '1'
#if not os.path.isdir(os.path.join(config.path_to_predicted_images, folder_name)):
#    os.mkdir(os.path.join(config.path_to_predicted_images, folder_name))
#BoxesAvgNums(folder_name, model, config)

