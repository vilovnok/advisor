import re

def extract_job_info(text):
    job_info_regex = r"Вакансия:\s([^\n]*)"
    match = re.search(job_info_regex, text)
    if match:
        return match.group(1)
    else:
        return 'Вакансия не найдена'