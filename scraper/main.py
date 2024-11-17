import os
import logging
import argparse
from scraper.parser import Parser


api_key = 'hIBq3oF9S5hz3YmoxEDmxK9OmZW91BSx'        
model = "mistral-large-latest"

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')


if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    print(f"Created directory: {data_dir}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", type=str, required=True)
    parser.add_argument("--area", type=str, required=True)
    parser.add_argument("--limit_page", type=str, required=True)
    parser.add_argument("--limit_objects", type=str, required=True)
    parser.add_argument("--only", type=str, required=False)
    args = parser.parse_args()

    area = args.area
    topic = args.topic
    limit_page = args.limit_page
    limit_objects = args.limit_objects
    only = args.only if args.only else 'all'

    parser = Parser(topic=topic, api_key=api_key, model=model, area=area)
    
    if only == 'cv':
        parser.create_file_cv(limit_page=limit_page, limit_objects=int(limit_objects))
        logging.info(f"CV: Все данные по {topic} получены.")
    elif only == 'vacancy':
        parser.create_file_vacancy(limit_page=limit_page, limit_objects=int(limit_objects))
        logging.info(f"Vacancy: Все данные по {topic} получены.")
    elif only == 'all':
        parser.create_file_cv(limit_page=limit_page, limit_objects=int(limit_objects))
        parser.create_file_vacancy(limit_page=limit_page, limit_objects=int(limit_objects))
        logging.info("CV+Vacancy: Все данные получены.")