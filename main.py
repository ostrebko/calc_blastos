import os
from utilits.functions import config_reader
#from utils.predict_wth_yolov5 import create_model, calc_boxes, calc_avg_num_blastos
from utilits.model_loader import LoadModel

path_to_config = 'config/data_config.json'
config = config_reader(path_to_config)

model = LoadModel(config).loaded_model
print(model.max_det)
