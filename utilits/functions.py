# Импортируем библиотеки
import os
import glob
import shutil
import string
import pandas as pd
from utilits.read_config import config_reader
from utilits.model_loader import LoadModel
from utilits.calcs_boxes import BoxesAvgNums


def clear_folder(path_to_folder):
    files_to_remove = glob.glob(os.path.join(path_to_folder, '*'))
    for f in files_to_remove:
        shutil.rmtree(f)


def create_report(config):
    path_to_pred_img = config.path_to_predicted_images
    names_pred_list = sorted(os.listdir(path_to_pred_img))
    
    col_start_rec = 0
    row_start_rec = 0
    max_col_in_row = config.bar_col_num * config.col_one_bar
    max_row_in_line = 0
    
    with pd.ExcelWriter('results.xlsx', engine='xlsxwriter') as writer:

        for fold_name in names_pred_list:
            csv_file = pd.read_csv(glob.glob(os.path.join(path_to_pred_img, fold_name,'*.csv'))[0],
                                   delimiter=';',
                                   names=['filename', 'all_calc', 'reduce_calc'],
                                   index_col=False)
            
            # создание одинакового отступа при смещении записи по строкам
            if len(csv_file) > max_row_in_line:
                max_row_in_line = len(csv_file)
            
            if col_start_rec//max_col_in_row==1: 
                # 1 столбец отчета - 3 столбца с данными + 2 пустых столбца
                col_start_rec = 0
                row_start_rec += max_row_in_line + 3
                max_row_in_line = len(csv_file)

            csv_file.to_excel(writer, 'Sheet1', 
                            startcol=col_start_rec, 
                            startrow=row_start_rec, 
                            header=['folder: '+ fold_name, 'all_calc', 'reduce_calc'],
                            index=False
                            )
            
            col_start_rec += config.col_one_bar
            
        
        workbook = writer.book
        worksheet = writer.sheets[config.worksheet_name]
        
        format_1 = workbook.add_format({'align': config.allign_param})
        format_2 = workbook.add_format({'border': config.border_param})

        last_col_for_row = string.ascii_uppercase[max_col_in_row-1]
        worksheet.set_column('A:' + last_col_for_row, 
                             config.col_wide, format_1) # Задаем ширину колонок с А по O 
        worksheet.conditional_format(0, 0,
                                     row_start_rec+max_row_in_line+3, max_col_in_row,
                                     {'type': 'cell',
                                     'criteria': '!=',
                                     'value': '$ZZ$1',
                                     'format': format_2}
                                     )
    print('Report created!!!')


def calc_avg_wth_crt_reprt(path_to_config): #='config/data_config.json'
    intro_text = ("This app allows to calculate "
                  "average number of blastospores on photos in one folder "
                  "or average number of blastospores on photos in multiple folder "
                  "with create report")
    print(intro_text)
    config = config_reader(path_to_config)
    model = LoadModel(config).loaded_model
    clear_folder(config.path_to_predicted_images)
    for fold_name in os.listdir(config.path_to_images):
        #if os.path.isdir(os.path.join(config.path_to_predicted_images, fold_name)):
        #    shutil.rmtree(os.path.join(config.path_to_predicted_images, fold_name))
        os.mkdir(os.path.join(config.path_to_predicted_images, fold_name))
        BoxesAvgNums(fold_name, model, config)
    create_report(config)
    print('Well done!!!')