# Импортируем библиотеки
import os
import shutil
from utilits.read_config import config_reader
from utilits.model_loader import LoadModel
from utilits.calcs_boxes import BoxesAvgNums


def calc_avg_num_blastos(path_to_config): #='config/data_config.json'
    config = config_reader(path_to_config)
    model = LoadModel(config).loaded_model
    for fold_name in os.listdir(config.path_to_images):
        if os.path.isdir(os.path.join(config.path_to_predicted_images, fold_name)):
            shutil.rmtree(os.path.join(config.path_to_predicted_images, fold_name))
        os.mkdir(os.path.join(config.path_to_predicted_images, fold_name))
        BoxesAvgNums(fold_name, model, config)
    print('Well done!!!')