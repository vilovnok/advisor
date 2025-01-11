import re
import yaml
from enum import Enum

class LlmModelType(Enum):
    LLAMA31 = "llama3.1"
    QWEN = "Qwen/Qwen2.5-7B-Instruct"

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


class PromptSanitizer:

    def __init__(self):
        pass
    def __sanitize(self, input_text: str, delimiter: str):
        """Удаляет опасные конструкции из текста."""

        sanitized_user_input = input_text.replace(delimiter, "")
        return f"{delimiter}\n{sanitized_user_input}\n{delimiter}"
    
    def __remove_hashes(self, input_text: str):
        cleaned_text = re.sub(r"[^\w\s\n]", "", input_text)
        return cleaned_text
    
    def fix_response(self, content: str):
        """Проверяет текст на соответствие правилам."""
        return re.sub(r'Answer.*|###.*', '', content, flags=re.DOTALL)
    
    def get_completion_from_messages(self, input_text, delimiter):
        """Проводит полную обработку текста."""

        cleaned_text = self.__remove_hashes(input_text=input_text)
        return self.__sanitize(cleaned_text, delimiter)

