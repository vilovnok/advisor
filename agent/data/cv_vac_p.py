import re
import logging
import requests
import fake_useragent
from tqdm import tqdm
from bs4 import BeautifulSoup
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


class CV_parser:
    """ Парсер для вакансий и CV """

    def __init__(self, cv_job, vac_job, area):
        api_key = 'hIBq3oF9S5hz3YmoxEDmxK9OmZW91BSx'        

        self.cv_job = cv_job
        self.area = area
        self.vac_job = vac_job
        self.mistral = self._get_mistral(api_key)


    def _get_mistral(self, api_key: str):
        mistral_chat = ChatMistralAI(
            model="mistral-large-latest",
            temperature=0.2,
            max_retries=2,
            api_key=api_key
        )
        return mistral_chat


    def _get_count_page_cv(self):
        """ Получаем количество страниц """
        
        cv_job = self.cv_job        
        ua = fake_useragent.UserAgent()
        
        url = f"https://hh.ru/search/resume?text={cv_job}&area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=false&page=1"
        data = requests.get(url=url, headers={"user-agent": ua.random})
        
        soup = BeautifulSoup(data.content, "lxml")
        page_count = int(soup.find("div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").find("span").text)
        
        return page_count


    def get_links_cv(self, ex_period=None, limit_page=None):
        """ Получаем ссылки на резюме пользователей """
        
        if not ex_period:
            raise ValueError('переменная ex_period не была передана. Пожалуйста, выбирите из предложенного перечня: "all_time"')
        
        area = self.area
        cv_job = self.cv_job
        ua = fake_useragent.UserAgent()
        resumes_links = []
        page_count = self._get_count_page_cv() if not limit_page else limit_page
        
        for page in tqdm(range(page_count), desc="Парсим CV ссылки"):  
            url=f"https://hh.ru/search/resume?text={cv_job}&area={area}&isDefaultArea=true&exp_period={ex_period}&logic=normal&pos=full_text&fromSearchLine=false&page={page}"
            data = requests.get(url=url, headers={"user-agent": ua.random})

            soup = BeautifulSoup(data.content, "lxml")                
            hrefs = [f'https://hh.ru/{a["href"]}' for a in soup.find_all("a", attrs={"data-qa": "serp-item__title"})]    
            jobs = [occ.text for occ in soup.find_all("span", attrs={"data-qa":"serp-item__title-text"})]                
            resumes_links.extend(list(zip(jobs, hrefs)))  
                  
        return resumes_links


    def _analysis_of_description_cv(self, description):
        """ Конкретизирует работу кандидата, выделяя важную информацию  """

        if not description:
            raise ValueError('переменная description не была передана. Пожалуйста, добавьте описание.')

        map_prompt = ChatPromptTemplate.from_messages(
        [("system", """
          Ты агент который конкретизирует описание работы кандидата. Избався от всей не нужной информации. Например, даты, название компаний и всего того, что не отражает опыт работы.
          Убери всю не важную информацию и сохрани информацию, которая будет описывать опыт кандидата.
          Отвечай в одну строчку на РУССКОМ ЯЗЫКЕ.
          Описание: {context}      
          """)])

        map_chain = map_prompt | self.mistral | StrOutputParser()
        result = map_chain.invoke({"context": description})

        return result.replace("\n", ". ")


    def get_info_cv(self, link=None):
        """ Получаем полную информацию о резюме пользователя """

        if not link:
            raise ValueError('переменная link не была передана. Пожалуйста, добавьте ссылку.')

        ua = fake_useragent.UserAgent()
        data = requests.get(url=link, headers={"user-agent": ua.random})
        soup = BeautifulSoup(data.content, "lxml")

        try:
            name = soup.find(attrs={"class": "resume-block__title-text"}).text
        except:
            name = ""
        try:
            experience = soup.find(attrs={"class": "resume-block__title-text_sub"}).text.replace(" ", " ").replace(" ", " ")
        except:
            experience = ""
        try:
            salary = soup.find(attrs={"class": "resume-block__title-text_salary"}).text.replace("\u2009", " ").replace(
                "\xa0", " ")
        except:
            salary = ""
        try:
            skills = ", ".join([skill.get_text(separator=' ', strip=True) for skill in soup.find(attrs={"class": "bloko-tag-list"}).find_all(attrs={"class": "bloko-tag__section_text"})])
        except:
            skills = [] 
        try:
            professional_roles = soup.find(attrs={"class": "resume-block__specialization"}).text
        except:
            professional_roles = ""    
        try:
            schedule_employment = [shell.get_text(separator=' ', strip=True) for shell in soup.find(attrs={"class": "resume-block-container"}).find_all("p")]
        except:
            schedule_employment = ""        
        try:
            language = ", ".join([lang.get_text(separator=' ', strip=True) for lang in soup.find_all(attrs={"data-qa": "resume-block-language-item"})])
        except:
            language = []
        try:
            education = ", ".join([edu.get_text(separator=' ', strip=True) for edu in soup.find_all(attrs={"data-qa": "resume-block-education"})])
        except:
            education = []
        try:
            location = ", ".join([loc.get_text(separator=' ', strip=True).replace("\xa0", " ") for loc in soup.find_all(attrs={"data-sentry-source-file": "ResumePersonalLocation.jsx"})])
        except:
            location = []
        try:
            description = " ".join([desc.get_text(separator=' ', strip=True).replace("\xa0", " ").replace("Показать еще"," ").replace("\n"," ") for desc in soup.find_all(attrs={"data-sentry-component": "ResumeExperience"})])
            description = self._analysis_of_description_cv(description)            
        except:
            description = []

        resume = {
            "name": name if name else None,                
            "salary": salary if salary else None,                
            "experience": experience if experience else None,        
            "description": description if description else None,
            "skills": skills if skills else None,
            'employment': schedule_employment[0].split(':')[-1] if schedule_employment else None,
            "schedule":  schedule_employment[1].split(':')[-1] if schedule_employment else None,
            "professional_roles": professional_roles if professional_roles else None,        
            "language": language if language else None,        
            "location":location if location else None,        
            "education": education if education else None,        
        }
        return resume        
        

    def to_file_cv(self, ex_period=None, limit_page=None):
        """ Получаем файл c СVs пользователей """
        
        if not ex_period:
            raise ValueError('переменная ex_period не была передана. Пожалуйста, выбирите из предложенного перечня: "all_time"')
        
        cv_job = self.cv_job
        resumes = []
        for _, link in tqdm(self.get_links_cv(ex_period=ex_period, limit_page=limit_page), desc="Парсим и обрабатываем CV"):
            resume = self.get_info_cv(link)
            resumes.append(resume)

        with open(f"CV_{cv_job}.txt", "w", encoding="utf-8") as f:
            for resume in tqdm(resumes):

                f.write(f"Ищет работу на должность: {resume['name']}\n")
                f.write(f"Желаемая зарплата: {resume['salary']}\n")
                f.write(f"Опыт работы: {resume['experience']}\n")
                f.write(f"Описание: {resume['description']}\n")                
                f.write(f"Ключевые навыки: {resume['skills']}\n")
                f.write(f"Тип занятости: {resume['employment']}\n")
                f.write(f"График работы: {resume['schedule']}\n")
                f.write(f"Знает языки: {resume['language']}\n")
                f.write(f"Образование: {resume['education']}\n")
                f.write(f"Местоположение: {resume['location']}\n")
                f.write(f"Профессиональные роли: {resume['professional_roles']}\n")
                f.write("\n" + "-" * 50 + "\n\n")
        
        logging.basicConfig(level=logging.INFO, filemode="w",format="%(asctime)s %(levelname)s: %(message)s")
        logging.info(f"Файл создан! Файл содержит CV кандидатов в количестве {len(resumes)}.")


    def get_vacancies(self, page):
        """ Получаем ссылки всех вакансий """

        area = self.area
        vac_job = self.vac_job
        params = {"text": vac_job, "area": area, "per_page": 100, "page": page, "order_by": "publication_time"}
        n_obj = []

        response = requests.get(url="https://api.hh.ru/vacancies", params=params)
        if response.status_code == 200:        
            vacancies = response.json()
            for vacancy in vacancies['items']:

                vacancy_id = vacancy['id']    
                vacancy_name = vacancy['name']
                vacancy_link = vacancy['alternate_url']
                vacancy_full_des = vacancy['url']

                n_obj.append((vacancy_id, vacancy_name, vacancy_link, vacancy_full_des))
            return n_obj
        elif response.status_code == 400:        
            return n_obj
        elif response.status_code == 443:        
            return None
        else:
            return None




    def get_links_vac(self, limit_page=None):
        """ Получаем ссылки на вакансии """
        
        all_data, page = [], 0

        while True:  
            
            n_obj = self.get_vacancies(page=page)            
            
            if len(n_obj) == 0:
                break        
            elif not n_obj:
                continue
            elif limit_page and (page == limit_page):
                break
            print(page)
            page+=1            
            all_data.extend(n_obj)

        return list(set(all_data))
    

    def prep_skills(self, skills):
        """ Подготовить строку для скилов """

        if not skills:
            return None
        sent = ''
        for skil in skills:
            sent+= f'{skil["name"]}, '
        sent = sent[:-2]+'.'

        return sent
    
    def _analysis_of_description_vac(self, description):
        """ Конкретизирует работу вакансии  """

        if not description:
            raise ValueError('переменная description не была передана. Пожалуйста, добавьте описание.')

        map_prompt = ChatPromptTemplate.from_messages(
        [("system", """
          Ты агент который помогает выделить самое главное из описания вакансий, обращая внимание на:
          1) Какие технологии использует компания и чем она занимается?
          2) Какие требования (ожидания) от кандидата?
          3) Чем будет заниматься кандидат в компании?
          4) Что предлагает компания?
          ВАЖНО: Если в вакансии какой либо информации не указано, то просто оставляй None.
          Избався от всей не нужной информации. Например, даты, название компаний и тд.
          Отвечай в одну строчку на РУССКОМ ЯЗЫКЕ.
          Описание: {context}      
          """)])

        map_chain = map_prompt | self.mistral | StrOutputParser()
        result = map_chain.invoke({"context": description})

        return result.replace("\n", ". ")



    def prep_description(self, description):
        """ Подготовить строку для описания описание """

        if not description:
            return None
        soup = BeautifulSoup(description, 'html.parser')
        text = soup.get_text(separator=' ')
        cleaned_text = re.sub(r'[\u200b\u200c\u200d\u2060\ufeff]', ' ', text)
        description = self._analysis_of_description_vac(cleaned_text)
        return description







    def get_info_vac(self, link):
        """ Получить полную информацию вакансию """
        try:  
            response = requests.get(link)
            info_vacancy = response.json()
        except:
            return None

        try:
            name = info_vacancy['name']
        except:
            name = None
        try:
            experience = info_vacancy['experience']['name']
        except:
            experience = None
        try:
            schedule = info_vacancy['schedule']['name']
        except:
            schedule = None
        try:
            employment = info_vacancy['employment']['name']
        except:
            employment = None
        try:
            description = info_vacancy['description']
        except:
            description = None
        try:
            skills = info_vacancy['key_skills']
        except:
            skills = None
        try:            
            professional_roles = info_vacancy['professional_roles'][0]['name']
        except:
            professional_roles = None

        full_info = {'name': name,
                     'experience': experience,
                     'description': description,
                     'skills': skills,
                     'employment': employment,
                     'schedule': schedule,
                     'professional_roles': professional_roles}

        return full_info 
    

    def to_file_vac(self, limit_page=None):
        """Создаем txt файл для всех вакансий с интервалом"""

        vac_job = self.vac_job
        vacancies = self.get_links_vac(limit_page)
        filename = f'{vac_job}_vacancies.txt'

        with open(filename, 'w') as f:
            for vacancy in tqdm(vacancies):

                vac_info = self.get_info_vac(vacancy[3])

                if vac_info is None:
                    continue
                
                skills = vac_info["skills"]
                title = self.prep_skills(skills=skills)
                description = self.prep_description(vac_info["description"])

                f.write(f'Имя вакансии: {vac_info["name"]}\n')
                f.write(f'Опыт работы: {vac_info["experience"]}\n')
                f.write(f'Описание: {description}\n')
                f.write(f'Ключевые навыки: {title}\n')
                f.write(f'Тип занятости: {vac_info["employment"]}\n')
                f.write(f'График работы: {vac_info["schedule"]}\n')
                f.write(f'Профессиональные роли: {vac_info["professional_roles"]}\n')
                f.write('\n' + '-' * 40 + '\n\n') 

        return filename
