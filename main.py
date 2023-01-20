import os
from utilits.functions import config_reader
from utilits.model_loader import LoadModel
from utilits.calcs_boxes import BoxesNums

path_to_config = 'config/data_config.json'
config = config_reader(path_to_config)

model = LoadModel(config).loaded_model

pathe = 'C:/Users/jaffa/Projects/calc_blastos/image_folder/1/1.jpg'
print(BoxesNums(pathe, model, config).num_boxes)
