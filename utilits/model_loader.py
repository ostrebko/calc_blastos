import os 
os.environ['TP_CPP_MIN_LOG_LEVEL']='2'

import sys
if not sys.warnoptions:
    import warnings
    warnings.simplefilter('ignore')

import torch


class LoadModel():
    
    """
    Decription ...
    
    Args:
    -------------
    config (_dict_) - словарь с конфигурацией
    ...
    """
    
    def __init__(self, config_json: dict):
        super().__init__()
        self.loaded_model = self.load_model(config=config_json)
        
    @staticmethod
    def load_model(config):
        
        if config.local_repo:
            if config.device=='cpu':
                model = torch.hub.load(config.path_to_yolov5, 
                                    config.model_type, 
                                    path=os.path.join(
                                        config.path_to_model, config.model_name),
                                    source='local', 
                                    device=config.device, 
                                    force_reload=config.force_reload)
            elif config.device=='gpu':
                model = torch.hub.load(config.path_to_yolov5, 
                                    config.model_type, 
                                    path=os.path.join(
                                        config.path_to_model, config.model_name),
                                    source='local', 
                                    force_reload=config.force_reload)

        else:
            model = torch.hub.load('ultralytics/yolov5', 
                                   config.model_type, 
                                   path=os.path.join(
                                       config.path_to_model, config.model_name), 
                                   device=config.device, 
                                   force_reload=config.force_reload)
        
        model.max_det = 2000
        
        return model
