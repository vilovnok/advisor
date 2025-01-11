import re
import json

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
    Резюме: {data.get('title', 'Не указано')}
    Срок работы: {data.get('experience', 'Не указано')}
    Описание: {data.get('description', 'Не указано')}
    Ключевые навыки: {', '.join(data.get('skills', []))}
    Тип занятости: {data.get('employment', 'Не указано')}
    График работы: {data.get('schedule', 'Не указано')}
    Знание языков: {', '.join([f"{lang['language']} — {lang['proficiency']}" for lang in data.get('languages', [])])}
    Образование: {data.get('education', 'Не указано')}
    """
    return summary.strip()

