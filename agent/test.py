import yaml

with open('config/env.yaml', 'r') as file:
    config = yaml.safe_load(file)


def get_model_info(model_name):
    for model in config['models']:
        if model['name'] == model_name:
            return model  
    return None  


selected_model_name = "Mistral"
model_info = get_model_info(selected_model_name)

if model_info:
    print(f"Selected Model: {model_info['name']}")
    print(f"API Key: {model_info['api_key']}")
else:
    print("Модель не найдена.")