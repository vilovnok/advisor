import pandas as pd

import requests
from torch.cuda import is_available

from typing import List, Union
from pathlib import Path
from enum import Enum

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models


class ModelType(Enum):
    RUBERT_TINY_2 = "cointegrated/rubert-tiny2"
    DEEPVK_USER = "deepvk/USER-bge-m3"


class Retriever:
    def __init__(self, 
                 model_type: ModelType, 
                 localhost: str='0.0.0.0',
                 port: int=6333,
                 dataset_dir: str='./dataset',
                 device: int = None
        ) -> None:

        self.dataset_dir = dataset_dir
        self._model_type = model_type   
        self._device = 0 if (device is None and is_available()) else device

        self._model = self._setup_model()        
        self._client = self._setup_database(localhost=localhost, port=port)
    

    def _setup_model(self):
        if self._model_type == ModelType.DEEPVK_USER:
            model = SentenceTransformer(
                ModelType.DEEPVK_USER.value,
                device=self._device
            )
        else:
            raise NotImplementedError()

        return model
    
    
    def _setup_database(self, localhost: str, port: int):        
        if not requests.get(f'http://{localhost}:{port}'):
            raise Exception(f'Qdrant server is not running at http://{localhost}:{port}')
            
        client = QdrantClient(location=localhost, port=port)

        return client


    def encode(self, text: Union[List[str], str]):
        if self._model_type == ModelType.DEEPVK_USER:
            embeddings = self._model.encode(text, normalize_embeddings=True)
        else:
            raise NotImplementedError()
        
        return embeddings
    
    def search(
            self,
            query: str,
            collection_name: str,
            topk: int = 10,
            filter_options: dict = None,
            score_threshold: float = None
        ):
        try:
            embedding = self.encode(query)
            results = self._client.search(
                collection_name,
                embedding,
                limit=topk,
                query_filter=models.Filter(
                    must=[
                        models.FieldCondition(key=k, match=models.MatchValue(value=v))
                        for k, v in filter_options.items()
                    ]
                ) if filter_options else None,
                score_threshold=score_threshold
            )

            return results
        finally:
            if hasattr(self._client, 'close'):
                self._client.close() 
    

    def create_database(self, embedding: list, collection_name: str=None):
        """ Create the database """
        try:
            if self._client.collection_exists(collection_name=collection_name):
                return

            self._client.create_collection(
                collection_name=collection_name,
                    vectors_config=models.VectorParams(
                    size=len(embedding),
                    distance=models.Distance.COSINE
                )
            )
        finally:
            if hasattr(self._client, 'close'):
                self._client.close() 


    def delete_database(self, collection_name: str):
        """ Delete the database """

        try:
            self._client.delete_collection(collection_name=collection_name)
        finally:
            if hasattr(self._client, 'close'):
                self._client.close() 
    
    def get_all_files(self):
        """ Получить все файла в директории dataset_dir """

        directory_path = Path(self.dataset_dir)
        return [str(file) for file in directory_path.rglob('*') if file.is_file()]
    
    def combined_df(self, files: List[str]) -> pd.DataFrame:
        """ Комбенируем все csv файлы """

        df_combined = pd.DataFrame()
        
        for file in files:
            df = pd.read_csv(file)
            df_combined = pd.concat([df_combined, df], ignore_index=True)
        
        return df_combined


    def upload_database(self, collection_name: str):
        """ Загружаем данные в database """

        try:
            files = self.get_all_files()
            df = self.combined_df(files)

            embeddings = self.encode(df["content"].to_list())
            for idx, row in df.iterrows():
                self._client.upsert(
                    collection_name=collection_name,
                    points=[
                        models.PointStruct(
                            id=idx,
                            vector=embeddings[idx],
                            payload={
                                "content": row["content"],
                                "category": row["category"],
                                'catalog': row["catalog"]
                            }
                        )
                    ]
                )
        finally:
            if hasattr(self._client, 'close'):
                self._client.close()     
