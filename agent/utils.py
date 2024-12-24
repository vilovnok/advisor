import yaml
from enum import Enum

class LlmModelType(Enum):
    OLLAMA = "ollama"
    # QWEN = 'Qwen/Qwen2.5-7B-Instruct'
    vLLM = 'vllm'

class EmbedModelType(Enum):
    DEEPVK_USER = "deepvk/USER-bge-m3"
    MiniLM = "sentence-transformers/all-MiniLM-L6-v2"
    BM25 = "Qdrant/bm25"
    BERT = "colbert-ir/colbertv2.0"
    # E5_LARGE = 'intfloat/multilingual-e5-large'
    # E5_LARGE_INSTRUCT = 'intfloat/multilingual-e5-large-instruct'


#TODO: насколько это нужно 
def get_model_info(model_name):
    with open('agent/config/env.yaml', 'r') as file:
        config = yaml.safe_load(file)
    for model in config['models']:
        if model['name'] == model_name:
            return model  
    return None  

def get_system_prompt():
    with open('agent/prompts/system_prompt.txt', 'r') as file:
        prompt = file.read()
    return prompt