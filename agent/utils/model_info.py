import yaml

with open('agent/config/env.yaml', 'r') as file:
    config = yaml.safe_load(file)


def get_model_info(model_name):
    for model in config['models']:
        if model['name'] == model_name:
            return model  
    return None  