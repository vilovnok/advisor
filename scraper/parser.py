import re
import logging
import requests
import fake_useragent
from tqdm import tqdm
from bs4 import BeautifulSoup
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


####################################################################
####################### BEGIN CV BEGIN #############################
####################################################################

class Parser:
    """ Парсер для вакансий и CV """

    def __init__(self, 
                 api_key: str=None, 
                 model: str=None, 
                 area: int=None, 
                 topic: str=None
        ):
        
        self.area = area
        self.topic = topic

        self._setup_model(api_key=api_key, model=model)

    def _setup_model(self, api_key: str = None, model: str = None):
        try:
            self.model = ChatMistralAI(model=model, temperature=0, max_retries=2, api_key=api_key)
        except Exception as error:    
            raise ValueError(f"Что-то не так с моделью:\n{error}")


    def _get_count_page_cv(self):
        """ Получаем количество страниц для CV """
        try:
            ua = fake_useragent.UserAgent()        
            url = f"https://hh.ru/search/resume?text={self.topic}&area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=false&page=1"

            data = requests.get(url=url, headers={"user-agent": ua.random})        
            soup = BeautifulSoup(data.content, "lxml")
            page_count = int(soup.find("div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").find("span").text)        
            return page_count
        except Exception as error:
            raise ValueError(f"Что-то не так на этапе парсинга страниц CV:\n{error}")


    def get_links_cv(self, ex_period: str=None, limit_page: int=None):
        """ Получаем ссылки для CV пользователей """
        
        if not ex_period:
            raise ValueError('Переменная ex_period не была передана. Пожалуйста, выбирите из предложенного перечня: "all_time", "noExperience".')
        
        area = self.area
        topic = self.topic
        ua = fake_useragent.UserAgent()

        resumes_links = []
        page_count = self._get_count_page_cv() if not limit_page else limit_page
        try:
            for page in tqdm(range(page_count), desc="CV: Парсим ссылки"):  
                url=f"https://hh.ru/search/resume?text={topic}&area={area}&isDefaultArea=true&exp_period={ex_period}&logic=normal&pos=full_text&fromSearchLine=false&page={page}"
                data = requests.get(url=url, headers={"user-agent": ua.random})

                soup = BeautifulSoup(data.content, "lxml")                
                hrefs = [f'https://hh.ru/{a["href"]}' for a in soup.find_all("a", attrs={"data-qa": "serp-item__title"})]    
                jobs = [occ.text for occ in soup.find_all("span", attrs={"data-qa":"serp-item__title-text"})]                
                resumes_links.extend(list(zip(jobs, hrefs)))  

            return resumes_links
        except Exception as error:
            raise ValueError(f"Что-то не так на этапе парсинга ссылок CV:\n{error}")


    def process_description(self, description, task_type):
        """
        Обрабатывает описание кандидата в зависимости от указанной задачи.

        :param description: текст описания для анализа.
        :param task_type: тип задачи (например, 'extract' или 'summary-desc').
        :return: результат обработки.
        """
        if not description:
            raise ValueError('Переменная description не была передана. Пожалуйста, добавьте описание.')

        prompts = {
            "extract-desc": """
            Проанализируйте текст и выделите только информацию о том, чем занимался пользователь (его обязанности и задачи). 
            Пример ответа:  
            Чем занимался: <опишите задачи и обязанности пользователя>  
            Текст для анализа:  
            {context}
            """,
            "summary-desc": """
            Проанализируйте текст и создайте краткую суммаризацию, которая содержит только основную информацию о работе пользователя. 
            Суммаризация должна быть краткой, понятной и содержать ключевые задачи и обязанности.  
            Пример ответа:  
            Пользователь занимался настройкой CI/CD процессов, администрированием серверов, управлением контейнерами и мониторингом систем.
            Текст для анализа:  
            {context}
            """,
            "classifier-employment": """
            Выделите и перечислите все упомянутые в тексте типы занятости в строгом порядке: полная занятость, частичная занятость, проектная работа, стажировка. Если тип занятости не указан в тексте, пропустите его. Если в тексте не упоминается ни один из известных типов занятости, укажите - .
            
            Возможные типы занятости:  
            - полная занятость  
            - частичная занятость  
            - проектная работа  
            - стажировка  
            
            Пример 1:  
            Текст: полная занятость, частичная занятость, проектная работа, стажировка
            Ответ: полная занятость, частичная занятость, проектная работа, стажировка
            
            Пример 2:  
            Текст: стажировка, проектная работа, частичная занятость
            Ответ: частичная занятость, проектная работа, стажировка            
            
            Текст для анализа:  
            {context}
            """,
            "classifier-schedule": """
            Выделите и перечислите все упомянутые в тексте графики работы в строгом порядке: полный день, сменный график, гибкий график, удаленная работа. Если график работы не указан в тексте, пропустите его. Если в тексте не упоминается ни один из известных графиков работы, укажите - .
            
            Возможные графики работы:  
            - полный день  
            - сменный график  
            - гибкий график  
            - удаленная работа  
            
            Пример 1:  
            Текст: полный день, гибкий график, удаленная работа
            Ответ: полный день, гибкий график, удаленная работа
            
            Пример 2:  
            Текст: удаленная работа, гибкий график
            Ответ: гибкий график, удаленная работа
            
            Текст для анализа:  
            {context}
            """,
            "classifier-edu": """
            Проанализируйте текст и определите тип образования пользователя. Укажите, является ли образование высшим или неоконченным, а также техническое оно или нет. Если невозможно определить информацию об образовании, укажите -.

            Пример 1:  
            Текст: "Окончил Московский государственный технический университет имени Баумана по специальности инженер."  
            Ответ: Высшее образование, техническое  

            Пример 2:  
            Текст: "Учился в Санкт-Петербургском университете, но не закончил."  
            Ответ: Неоконченное высшее образование, нетехническое  

            Пример 3:  
            Текст: "Получил степень бакалавра в области компьютерных наук."  
            Ответ: Высшее образование, техническое  

            Пример 4:  
            Текст: "Образование в тексте не указано."  
            Ответ: -  

            Текст для анализа:  
            {context}
            """,            
        }

        if task_type not in prompts:
            raise ValueError(f"Неподдерживаемый тип задачи: {task_type}")

        try:
            prompt_text = prompts[task_type]
            prompt = ChatPromptTemplate.from_messages([("system", prompt_text)])
            chain = prompt | self.model | StrOutputParser()
            result = chain.invoke({"context": description})
            return result
        except Exception as error:
            raise ValueError(f"Что-то не так на этапе обработки описания CV:\n{error}")

    def cleaner_cv(self, description):
        """ Очищает неважную информацию о кандидате. """
        return self.process_description(description, task_type="extract-desc")

    def summary_cv(self, description):
        """ Создает краткую суммаризацию описания кандидата. """
        return self.process_description(description, task_type="summary-desc")
    def classifier_employment_cv(self, description):
    
        """ Создает краткую суммаризацию описания кандидата. """
        return self.process_description(description, task_type="classifier-employment")
    
    def classifier_schedule_cv(self, description):
        """ Создает краткую суммаризацию описания кандидата. """
        return self.process_description(description, task_type="classifier-schedule")
    
    def classifier_edu_cv(self, description):
        """ Создает краткую суммаризацию описания кандидата. """
        return self.process_description(description, task_type="classifier-edu")


    def get_user_cv(self, link=None):
        """ Получаем CV кандидата """

        if not link:
            raise ValueError('Переменная link не была передана. Пожалуйста, добавьте ссылку.')

        ua = fake_useragent.UserAgent()
        data = requests.get(url=link, headers={"user-agent": ua.random})
        soup = BeautifulSoup(data.content, "lxml")

        try:
            name = soup.find(attrs={"class": "resume-block__title-text"}).text
        except:
            raise ValueError('Invalid value')
        try:
            experience = soup.find(attrs={"class": "resume-block__title-text_sub"}).text.replace(" ", " ").replace(" ", " ").split('работы')[-1]
            if not any(char.isdigit() for char in experience):
                ValueError('Invalid value')
        except:
            raise ValueError('Invalid value')            
        try:
            skills = ", ".join([skill.get_text(separator=' ', strip=True) for skill in soup.find(attrs={"class": "bloko-tag-list"}).find_all(attrs={"class": "bloko-tag__section_text"})])
        except:
            raise ValueError('Invalid value')
        try:
            professional_roles = soup.find(attrs={"class": "resume-block__specialization"}).text
        except:
            professional_roles = '-'   
        try:
            schedule_employment = [shell.get_text(separator=' ', strip=True) for shell in soup.find(attrs={"class": "resume-block-container"}).find_all("p")]
            employment = schedule_employment[0].split(':')[-1]
            schedule = schedule_employment[1].split(':')[-1]

            employment = self.classifier_employment_cv(employment)            
            schedule = self.classifier_schedule_cv(schedule)
        except:
            employment, schedule = '-', '-'       
        try:
            language = ", ".join([lang.get_text(separator=' ', strip=True) for lang in soup.find_all(attrs={"data-qa": "resume-block-language-item"})])
        except:
            language = '-'
        try:
            education = ", ".join([edu.get_text(separator=' ', strip=True) for edu in soup.find_all(attrs={"data-qa": "resume-block-education"})])
            education = self.classifier_edu_cv(education)
        except:
            education = '-'

        try:
            location = ", ".join([loc.get_text(separator=' ', strip=True).replace("\xa0", " ") for loc in soup.find_all(attrs={"data-sentry-source-file": "ResumePersonalLocation.jsx"})])            
        except:
            location = '-'
        try:
            description = soup.find_all(attrs={"data-qa": "resume-block-experience"})
            description = self.cleaner_cv(description)            
            description = self.summary_cv(description)            
        except:
            raise ValueError('Invalid value')


        resume = {
            "name": name,                                
            "experience": experience,
            "description": description,
            "skills": skills,
            'employment': employment,
            "schedule":  schedule,
            "professional_roles": professional_roles,
            "language": language,
            "location": location,
            "education": education,
        }
        return resume        
        

    def create_file_cv(self, ex_period:str='all_time', limit_page:str=None, limit_objects: int=None,):
        """ Получаем файл c СVs """
        
        resumes = []
        if not ex_period:
            raise ValueError('Переменная ex_period не была передана. Пожалуйста, выбирите из предложенного перечня: "all_time", "noExperience".')
                
        try:
            links = self.get_links_cv(ex_period=ex_period, limit_page=int(limit_page))
            
            if len(links) < limit_objects: limit_objects = None

            for _, link in tqdm(links[:limit_objects], desc="CV: Создаем файл"):
                try:
                    resume = self.get_user_cv(link)
                except Exception as error:                    
                    continue
                resumes.append(resume)    
            with open(f"data/CV_{self.topic}.txt", "w", encoding="utf-8") as f:
                for resume in tqdm(resumes):

                    f.write(f"Резюме: {resume['name']}\n")
                    f.write(f"Опыт работы: {resume['experience']}\n")
                    f.write(f"Описание: {resume['description']}\n")                
                    f.write(f"Ключевые навыки: {resume['skills']}\n")
                    f.write(f"Тип занятости: {resume['employment']}\n")
                    f.write(f"График работы: {resume['schedule']}\n")
                    f.write(f"Знание языков: {resume['language']}\n")
                    f.write(f"Образование: {resume['education']}\n")
                    # f.write(f"Местоположение: {resume['location']}\n")
                    f.write("\n" + "-" * 50 + "\n\n")

            logging.basicConfig(level=logging.INFO, filemode="w",format="%(asctime)s %(levelname)s: %(message)s")
            logging.info(f"Файл создан! Файл содержит CV кандидатов в количестве {len(resumes)}.")
        except Exception as error:
            raise ValueError(f"Что-то не так на этапе создания файла с CVs:\n{error}")

####################################################################
####################### END CV END #################################
####################################################################

    def get_vacancies(self, page):
        """ Получаем информацию о вакансиях """
        
        n_obj = []
        params = {"text": self.topic, "area": self.area, "per_page": 100, "page": page, "order_by": "publication_time"}
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

            page+=1            
            all_data.extend(n_obj)
        return list(set(all_data))
    

    def prep_skills(self, skills):
        """ Подготовить строку для скилов """

        if not skills:
            return 'unknown'
        sent = ''
        for skil in skills:
            sent+= f'{skil["name"]}, '
        sent = sent[:-2]+'.'

        return sent
    
    def cleaner_vacancy(self, description):
        """ Очищает не важную информацию в вакансии """

        if not description:
            raise ValueError('переменная description не была передана. Пожалуйста, добавьте описание.')
        try:
            prompt = ChatPromptTemplate.from_messages(
            [("system", """
              Ты агент который помогает выделить самое главное из описания вакансий, обращая внимание на:
              
              Описание: Чем компания занимается, какие технологии использует, что она предлагает и какие требования (ожидания) от кандидата?
              Знание языка: какие языки требуются?
              Образование: требуется или не требуеться ?        
              
              ВАЖНО: Если в вакансии какой либо информации не указано, то просто оставляй None.
              Избався от всей не нужной информации. Например, даты, название компаний и тд.
              В область "знание языка" должно входить языки естественной речи (просто укажи если есть в описание).
                            
              Описание: {context}      
              Твой ответ должен быть в одну строку (содержания описание, знание языка и образование должны быть разделены $):
              """)])

            chain = prompt | self.model | StrOutputParser()
            result = chain.invoke({"context": description})

            return result.replace("\n", ". ")
        except Exception as error:
            raise ValueError(f"Что-то не так на этапе очистки описания Vacany:\n{error}")



    def prep_description(self, description):
        """ Подготовить строку для описания описание """

        if not description:
            return None
        soup = BeautifulSoup(description, 'html.parser')
        text = soup.get_text(separator=' ')
        cleaned_text = re.sub(r'[\u200b\u200c\u200d\u2060\ufeff]', ' ', text)
        description = self.cleaner_vacancy(cleaned_text)
        return description


    def get_info_vacancy(self, link):
        """ Получаем полную информацию о вакансии """

        try:  
            response = requests.get(link)
            info_vacancy = response.json()
        except:
            raise ValueError('Invalid value')
        try:
            name = info_vacancy['name']
        except:
            raise ValueError('Invalid value')
        try:
            address = info_vacancy['address']['city']
        except:
            address = '-'            
        try:
            experience = info_vacancy['experience']['name']
        except:
            raise ValueError('Invalid value')
        try:
            schedule = info_vacancy['schedule']['name']
        except:
            schedule = '-'
        try:
            employment = info_vacancy['employment']['name']
        except:
            employment = '-'            
        try:
            description = info_vacancy['description']
        except:
            raise ValueError('Invalid value')
        try:
            skills = info_vacancy['key_skills']
        except:
            raise ValueError('Invalid value')
        # try:            
        #     professional_roles = info_vacancy['professional_roles'][0]['name']
        # except:
        #     professional_roles = None
        #     raise ValueError('Invalid value')

        full_info = {'name': name,
                     'experience': experience,
                     'description': description,
                     'address': address,
                     'skills': skills,
                     'employment': employment,
                     'schedule': schedule,                     
                    #  'professional_roles': professional_roles
                     }

        return full_info 
    

    def create_file_vacancy(self, limit_page: int=None, limit_objects: int=None):
        """Создаем txt файл для всех вакансий с интервалом"""

        vacancies = self.get_links_vac(limit_page)
        filename = f'data/VAC_{self.topic}.txt'

        if len(vacancies) < limit_objects: limit_objects = None

        with open(filename, 'w') as f:
            for vacancy in tqdm(vacancies[:limit_objects], desc="Vacancy: Создаем файл"):  
                try:
                    vac_info = self.get_info_vacancy(vacancy[3])
                    
                    skills = vac_info["skills"]
                    title = self.prep_skills(skills=skills)
                    description = self.prep_description(vac_info["description"])
                    description, language, education = description.split("$")                                        
                    education = True if 'None' not in education else '-'
                    language = language if 'None' not in language else '-'

                    f.write(f'Вакансия: {vac_info["name"]}\n')
                    f.write(f'Опыт работы: {vac_info["experience"]}\n')
                    f.write(f'Описание: {description}\n')
                    f.write(f'Ключевые навыки: {title}\n')
                    f.write(f'Тип занятости: {vac_info["employment"]}\n')
                    f.write(f'График работы: {vac_info["schedule"]}\n')
                    f.write(f"Знание языков: {language}\n")
                    f.write(f"Образование: {education}\n")
                    # f.write(f"Местоположение: {vac_info['address']}\n")
                    f.write('\n' + '-' * 50 + '\n\n') 
                except Exception as error:
                    continue
        
        logging.basicConfig(level=logging.INFO, filemode="w",format="%(asctime)s %(levelname)s: %(message)s")
        logging.info(f"Файл создан! Файл содержит вакансии в количестве {len(vacancies[:limit_objects])}.")
        return filename
