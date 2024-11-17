from agent.database.retriever import Retriever, ModelType
import argparse
import logging



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("--act", type=str, required=True)
    parser.add_argument("--coll_name", type=str, required=True)
    args = parser.parse_args()

    act = args.act
    coll_name = args.coll_name
    
    retriever = Retriever(model_type=ModelType.DEEPVK_USER, device=0)

    if act == "create":
        embedding = retriever.encode(text='Hello, world')
        retriever.create_database(collection_name=coll_name, embedding=embedding)    
        logging.info("Коллекция создана!")    
    elif act == "delete":
        retriever.delete_database(collection_name=coll_name)
        logging.info("Коллекция удалена!")    
    elif act == "upload":
        retriever.upload_database(collection_name=coll_name)
        logging.info("Коллекция обновилась!")  
    elif act == "search":
        result = retriever.search(
        query = """Имя вакансии: DevOps (Middle+ / Senior)
                  Опыт работы: От 3 до 6 лет
                  Описание: Компания использует технологии: CI/CD (TeamCity, Jenkins), мониторинг (Zabbix, Prometheus, Grafana), автоматизация (Ansible, Terraform/OpenTofu), виртуализация (Docker, Kubernetes), ОС (Debian Linux), СУБД (PostgreSQL, MySQL, Clickhouse), Message Broker (RabbitMQ), Reverse proxy/web server (Nginx), прочие инструменты (Jira, Confluence, Git). Требования: опыт работы с большинством из перечисленных технологий или готовность их изучить. Кандидат будет заниматься поддержкой и развитием CI/CD, мониторинга, автоматизацией административных задач, развитием инфраструктуры на Linux, внедрением контейнеризации, взаимодействием с разработчиками и тестировщиками. Компания предлагает: гибкий график работы, офис или гибридный формат, стабильность, ДМС, социальную поддержку, развитие, компенсацию обучения, корпоративы, тимбилдинги, удобные рабочие места, безлимитную еду.
                  Ключевые навыки: None
                  Тип занятости: Полная занятость
                  График работы: Полный день
                  Местоположение: Москва
                  Профессиональные роли: DevOps-инженер""",
        collection_name = "it_area",
        topk=4,
        filter_options={"category": "devops", 'catalog':'cv'}
        )

        for i in result:
            print(i.payload['content'])
            print('--------------------------------')