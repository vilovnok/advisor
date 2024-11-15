import os, re

import asyncio
import aiofiles

from typing import List, Union
from datasets import Dataset

class ForgeDataset():
    """ Формируем dataset """
    
    def __init__(self, 
                 dataset_dir: str='dataset', 
                 api_key: str=None, 
                 model: str=None, 
                 topic: str=None
        ):
        
        self.dataset_dir = dataset_dir

        self.SYNONYMS = {
        'backend': ['backend', 'бекэнд', 'бэкенд', 'go', 'golang'],
        'frontend': ['frontend', 'фронтенд', 'web', 'веб', 'фронтэнда'],
        'devops': ['devops', 'девопс']
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
        Ищет все документы в директории `dataset_dir`.
        
        :param extensions: Список расширений файлов для фильтрации (например, ['.txt', '.pdf']).
        :return: Список путей к найденным файлам для CV и VAC.
        """

        CV_documents = []
        VAC_documents = []

        path = os.path.abspath(os.path.join(self.dataset_dir))
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
    
    # def write_document(self, path):
    #     """ Читаем документ """
        
    #     with open(path,'r+') as file:
    #         content = file.read()
        
    #     return content

    def forge(self, content: str, pertain: str):
        """ Классифицируем контент в файле """   

        if pertain == 'vac': 
            match=r'Имя вакансии: (.*?)\n'
        else:
            match = r'Ищет работу на должность: (.*?)\n'

        topics = []
        clasters = dict()     
        blocks = content.split('-' * 50)

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


    def run(self):
        """ Кластеризуем все  """
        
        # находим документы
        documents = self.fetch_documents(extensions=['.txt'])

        cv_content  = {} 
        vac_content = {} 

        # читаем документы
        # for document in documents['cv']:
        #     content = self.read_document(document)
        #     forge = self.forge(content=content, pertain='cv')            
        #     cv_content = self.update_clasters(claster=forge['clasters'], content=cv_content)

        
        for document in documents['vac']:
            print(document)
            content = self.read_document(document)            
            forge = self.forge(content=content, pertain='vac')            
            vac_content = self.update_clasters(claster=forge['clasters'], content=vac_content)
        
        return {'cv_content': cv_content, 'vac_content': vac_content}


forge = ForgeDataset()
documents = forge.run()

# count=0
# for i in documents['vac_content'].keys():
    
#     item = documents['vac_content'][i]
#     count+=len(item)

# count=0
# for i in documents['cv_content']['backend']:
#     count+=1
# print(count)
