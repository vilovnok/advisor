import os, re
import pandas as pd
from datetime import datetime
from typing import List, Union
from datasets import Dataset
from scraper.utils import Mixin


class ForgeDataset(Mixin):
    """ Формируем dataset """
    
    def __init__(self, 
                data_dir: str='data', 
                dataset_dir: str='./dataset',
                api_key: str=None, 
                model: str=None, 
                topic: str=None
        ):
        
        self.dataset_dir = dataset_dir
        self.data_dir = data_dir

        self.SYNONYMS = {
        'backend': ['backend', 'бекэнд', 'бэкенд', 'go', 'golang', 'back end'],
        'frontend': ['frontend', 'фронтенд', 'web', 'веб', 'фронтэнда', 'front end'],
        'devops': ['devops', 'девопс'],
        'аналитик': ['аналитик','analyst'],
        'nlp': ['nlp','llm','rag','ml engineer','engineer'],
        'researcher': ['researcher', 'data scientist','deep learning engineer','software'],
        'manager': ['manager','lead']
    }


    def classification_object(self, topic: str) -> Union[str, tuple]:
        
        topic = topic.lower().replace('-', ' ')
        for standard_topic, synonyms in self.SYNONYMS.items():
            if any(synonym in topic for synonym in synonyms):
                return standard_topic

        return topic
    
    def classify_file_by_name(self, filename: str) -> str:
        extract = filename.replace('_', ' ').replace('/',' ')        
        if 'CV' in extract: return 'CV' 
        else: return 'VAC'


    def fetch_documents(self, extensions: List[str] = None) -> List[str]:
        """
        Ищет все документы в директории `data_dir`.
        
        :param extensions: Список расширений файлов для фильтрации (например, ['.txt', '.pdf']).
        :return: Список путей к найденным файлам для CV и VAC.
        """

        CV_documents = []
        VAC_documents = []

        path = os.path.abspath(os.path.join(self.data_dir))
        for root, _, files in os.walk(path):            
            for file in files:
                if extensions is None or any(file.endswith(ext) for ext in extensions):
                    if self.classify_file_by_name(file) == 'CV':    
                        CV_documents.append(os.path.join(root, file))
                    elif self.classify_file_by_name(file) == 'VAC':  
                        VAC_documents.append(os.path.join(root, file))  
                    else:
                        continue

        return {'cv':CV_documents,'vac':VAC_documents}


    def read_document(self, path):
        """ Читаем документ """
        
        with open(path,'r+') as file:
            content = file.read()
        
        return content
    
    
    def cluster_content_by_position(self, content: str, pertain: str):
        """ Кластеризируем контент """   

        if pertain == 'vac': 
            match=r'Вакансия: (.*?)\n'
        else:
            match = r'Резюме: (.*?)\n'

        topics = []
        clasters = dict()     
        blocks = re.split(r'-{3,}', content)

        for block in blocks:
            
            position_match = re.search(match, block)
            if not position_match: continue

            topic = position_match.group(1)
            class_obj = self.classification_object(topic=topic)            
            clasters[class_obj] = clasters.get(class_obj, []) + [block.strip()]
            topics.append(class_obj)        

        topics = [topic.lower().replace('-',' ') for topic in topics]
        unique_topics = list(set(topics))
        
        return {'clasters': clasters, 'unique_topics': unique_topics}
        

    def update_clasters(self, claster, content):
        """ Обновляем кластеры """
        
        for key in claster.keys():
            if key in content:
                content[key].extend(claster[key])
            else:
                content[key] = claster[key]

        return content
    
    def filter_content(self, content: dict, limit: int):
        """
        Ограничивает количество элементов в списке значений словаря до limit.
        Удаляет ключи, если длина их значений меньше limit.

        :param d: Исходный словарь
        :param limit: Максимальное количество элементов, которое должно остаться в списке
        :return: Обновленный словарь
        """

        result = {}
        for key, value in content.items():
            if len(value) >= limit:
                result[key] = value[:limit]

        return result


    def run(self, limit: int=50):
        """ Формируем контент  """
        
        # находим документы
        documents = self.fetch_documents(extensions=['.txt'])

        cv_content  = {} 
        vac_content = {} 

        # читаем документы
        for document in documents['cv']:
            content = self.read_document(document)
            extract = self.cluster_content_by_position(content=content, pertain='cv')            
            cv_content = self.update_clasters(claster=extract['clasters'], content=cv_content)
        
        # cv_content = self.filter_content(cv_content, limit)
        
        for document in documents['vac']:
            content = self.read_document(document)            
            extract = self.cluster_content_by_position(content=content, pertain='vac')            
            vac_content = self.update_clasters(claster=extract['clasters'], content=vac_content)
        
        # vac_content = self.filter_content(vac_content, limit)
        
        return {'cv_content': cv_content, 'vac_content': vac_content}


    def dataset(self, content: dict):
        """ Создаем датасеты как для CV и VAC """
        
        cv_dataset = Dataset.from_dict(content['cv_content'])
        vac_dataset = Dataset.from_dict(content['vac_content'])

        return cv_dataset, vac_dataset

    def save_to_disk(self, dataset: Dataset, filename: str, swich: int='cv'):
        """ Сохраняем датасеты на диск """
        if swich == 'cv':
            dataset.save_to_disk(f'{self.dataset_dir}/cv_dataset_{filename}')
        elif swich == 'vac':
            dataset.save_to_disk(f'{self.dataset_dir}/vac_dataset_{filename}')

    def save_to_csv(self, dataset: dict, filename: str, swich: int='cv'):
        """ Сохраняем контент в csv file """

        if swich == 'cv':
            file_path = f'{self.dataset_dir}/cv_dataset_{filename}.csv'
        elif swich == 'vac':
            file_path = f'{self.dataset_dir}/vac_dataset_{filename}.csv'

        rows = []
        for category, contents in dataset.items():
            rows.extend({"catalog": swich, "category": category, "content": content} for content in contents)

        df = pd.DataFrame(rows)

        df['url'], df['content'] = zip(*df['content'].apply(self.extract_and_remove_url))
        
        df.to_csv(file_path, index=False, encoding="utf-8")
        print(f"CSV файл успешно создан: {file_path}")


        

forge = ForgeDataset()

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dataset')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    print(f"Created directory: {data_dir}")


current_date = datetime.now()
formatted_date = current_date.strftime("%Y-%m-%d")

documents = forge.run(limit=20)

forge.save_to_csv(documents['vac_content'], f'{formatted_date}', 'vac')
forge.save_to_csv(documents['cv_content'], f'{formatted_date}', 'cv')