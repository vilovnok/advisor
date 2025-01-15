from agent.database.retriever import Retriever
from agent.utils import EmbedModelType

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
    
    retriever = Retriever(device=0)

    if act == "create":

        dense_embeddings = {}
        dense_embeddings[EmbedModelType.MiniLM] = retriever.encode(text='Hello, world', model_type=EmbedModelType.MiniLM)
        dense_embeddings[EmbedModelType.TOCHKA] = retriever.encode(text='Hello, world', model_type=EmbedModelType.TOCHKA)        
        dense_embeddings[EmbedModelType.E5_LARGE] = retriever.encode(text='Hello, world', model_type=EmbedModelType.E5_LARGE)       
        dense_embeddings[EmbedModelType.DEEPVK_USER] = retriever.encode(text='Hello, world', model_type=EmbedModelType.DEEPVK_USER)        
        dense_embeddings[EmbedModelType.RUBERT_TINY2] = retriever.encode(text='Hello, world', model_type=EmbedModelType.RUBERT_TINY2)        
        
        late_interaction_embeddings = retriever.encode(text=['Hello, world'], model_type=EmbedModelType.BERT)
        late_interaction_embeddings = list(late_interaction_embeddings)

        retriever.create_database(collection_name=coll_name, 
                                dense_embeddings=dense_embeddings,
                                late_interaction_embeddings=late_interaction_embeddings)    
        logging.info("Коллекция создана!")    
    elif act == "delete":
        retriever.delete_database(collection_name=coll_name)
        logging.info("Коллекция удалена!")    
    elif act == "upload":
        retriever.upload_db(collection_name=coll_name)
        logging.info("Коллекция обновилась!")  
    elif act == "search":
        result = retriever.search(
        query = """Резюме: DevOps engineer
                Work experience 5 years
                Описание: unknown
                Ключевые навыки: Linux, Docker, Bash, Ansible, SQL, Jenkins, Unix, DevOps, OpenShift, Git, Gitlab, Администрирование, Kubernetes
                Тип занятости: unknown
                График работы: unknown
                Знание языков: Russian — Native, English — B1 — Intermediate
                Образование: False
                """,
        collection_name = coll_name,
        topk=8,
        # filter_options={"category": "devops", 'catalog':'vac'}
        )

        for i in result:
            print(i.score)
            print(i.payload['content'])
            print('\n--------------------------------\n')