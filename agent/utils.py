import re
import json
from enum import Enum

class LlmModelType(Enum):
    LLAMA31 = "llama3.1"
    QWEN = "Qwen/Qwen2.5-7B-Instruct"

class EmbedModelType(Enum):
    DEEPVK_USER = "deepvk/USER-bge-m3"
    MiniLM = "sentence-transformers/all-MiniLM-L6-v2"
    BM25 = "Qdrant/bm25"
    BERT = "colbert-ir/colbertv2.0"
    TOCHKA = "Tochka-AI/ruRoPEBert-e5-base-2k"
    E5_LARGE = 'intfloat/multilingual-e5-large'
    RUBERT_TINY2 = "cointegrated/rubert-tiny2"


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


def validate_response(func):
    def wrapper(content: str):
        content = func(content)
        content = re.sub(r'(\{[^}]*\}).*', r'\1', content, flags=re.DOTALL)
        content = re.sub(r'Answer.*|###.*|soft_skills[^]]*$', '', content, flags=re.DOTALL)
        content = re.sub(r"'", '"', content)
        content = re.sub(r'([{,])\s*([a-zA-Z0-9_]+)\s*:', r'\1"\2":', content)
        try:            
            return json.loads(content) 
        except json.JSONDecodeError:
            return
    return wrapper


@validate_response
def conv_to_json(content: str):
    return content

def generate_summary(data: json):
    summary = f"""
    Опыт работы: {data.get('experience', 'Не указано')}
    Описание: {data.get('description', 'Не указано')}
    Ключевые навыки: {data.get('skills', 'Не указано')}
    Тип занятости: {data.get('employment', 'Не указано')}
    График работы: {data.get('schedule', 'Не указано')}
    Знание языков: {data.get('language', 'Не указано')}
    Образование: {data.get('education', 'Не указано')}
    """
    return summary.strip()
