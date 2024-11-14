import logging
import argparse
from parser import Parser


api_key = 'hIBq3oF9S5hz3YmoxEDmxK9OmZW91BSx'        
model = "mistral-large-latest"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", type=str, required=True)
    parser.add_argument("--area", type=str, required=True)
    parser.add_argument("--ex_period", type=str, required=True)
    parser.add_argument("--limit_page", type=str, required=True)
    parser.add_argument("--only", type=str, required=False)
    args = parser.parse_args()

    area = args.area
    topic = args.topic
    ex_period = args.ex_period
    limit_page = args.limit_page

    only = args.only
    if not only:
        only = 'all'

    parser = Parser(topic=topic, api_key=api_key, model=model, area=area)
    
    if only == 'cv':
        parser.create_file_cv(ex_period=ex_period, limit_page=limit_page)
        logging.info(f"CV: Все данные по {topic} получены.")
    elif only == 'vacancy':
        parser.create_file_vacancy(limit_page=limit_page)
        logging.info(f"Vacancy: Все данные по {topic} получены.")
    elif only == 'all':
        parser.create_file_cv(ex_period=ex_period, limit_page=limit_page)
        parser.create_file_vacancy(limit_page=limit_page)
        logging.info("CV+Vacancy: Все данные получены.")