import re

def extract_job_info(text):
    patterns = {
        "Вакансия": r"Вакансия:\s([^\n]*)",
        "Резюме": r"Резюме:\s([^\n]*)"
    }
    
    for _, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    
    return 'не найдено'