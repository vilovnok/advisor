import tqdm
import requests
import pandas as pd
from datasets import Dataset
from typing import List, Union
from torch.cuda import is_available
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

from agent.database.utils import Mixin, ModelEncoder
from agent.utils import EmbedModelType
from fastembed.late_interaction import LateInteractionTextEmbedding
from fastembed.sparse.bm25 import Bm25


class Retriever(Mixin):
    def __init__(self, 
        localhost: str='0.0.0.0',
        port: int=6333,
        dataset_dir: str='./dataset',
        device: int = None
        ) -> None:

        self.dataset_dir = dataset_dir
        self._device = 0 if (device is None and is_available()) else device
        self._client = self._setup_database(localhost=localhost, port=port)    

    def _setup_database(self, localhost: str, port: int):        
        if not requests.get(f'http://localhost:6333'):
            raise Exception(f'Qdrant server is not running at http://{localhost}:{port}')
            
        client = QdrantClient(location=localhost, port=6333)
        return client

    def _setup_model(self, model_type: EmbedModelType):        
        if model_type == EmbedModelType.DEEPVK_USER:
            model = SentenceTransformer(
                    EmbedModelType.DEEPVK_USER.value,
                    device=self._device
                )
        elif model_type == EmbedModelType.RUBERT_TINY2:
            model = SentenceTransformer(
                    EmbedModelType.RUBERT_TINY2.value,
                    device=self._device
                )
            
        elif model_type == EmbedModelType.MiniLM:
            model = SentenceTransformer(
                    EmbedModelType.MiniLM.value,
                    device=self._device
                )
            
        elif model_type == EmbedModelType.BM25:
            model = Bm25(EmbedModelType.BM25.value)

        elif model_type == EmbedModelType.BERT:                
            model = LateInteractionTextEmbedding(EmbedModelType.BERT.value)

        elif model_type == EmbedModelType.TOCHKA:
            model = ModelEncoder(model_name=EmbedModelType.TOCHKA)

        elif model_type == EmbedModelType.E5_LARGE:
            model = ModelEncoder(model_name=EmbedModelType.E5_LARGE)

        return model


    def encode(self, text: Union[List[str], str], model_type: EmbedModelType=None):
        try:
            if model_type == EmbedModelType.DEEPVK_USER:
                embeddings = SentenceTransformer(
                    EmbedModelType.DEEPVK_USER.value,
                    device=self._device
                ).encode(text, normalize_embeddings=True)

            elif model_type == EmbedModelType.RUBERT_TINY2:
                embeddings = SentenceTransformer(
                    EmbedModelType.RUBERT_TINY2.value,
                    device=self._device
                ).encode(text, normalize_embeddings=True)

            elif model_type == EmbedModelType.MiniLM:
                embeddings = SentenceTransformer(
                    EmbedModelType.MiniLM.value,
                    device=self._device
                ).encode(text, normalize_embeddings=True)
            
            elif model_type == EmbedModelType.BM25:                
                bm25_embedding_model = Bm25(EmbedModelType.BM25.value)
                embeddings = bm25_embedding_model.passage_embed(text)
            
            elif model_type == EmbedModelType.BERT:
                late_interaction_embedding_model = LateInteractionTextEmbedding(EmbedModelType.BERT.value)
                embeddings = late_interaction_embedding_model.passage_embed(text)
            
            elif model_type == EmbedModelType.TOCHKA:
                embeddings = SentenceTransformer(
                    EmbedModelType.TOCHKA.value,
                    device=self._device
                ).encode(text, normalize_embeddings=True)

            elif model_type == EmbedModelType.E5_LARGE:
                embeddings = ModelEncoder(model_name=EmbedModelType.E5_LARGE).encode(text=text)
            
            elif model_type == EmbedModelType.TOCHKA:
                embeddings = ModelEncoder(model_name=EmbedModelType.TOCHKA).encode(text=text)

            else:
                raise ValueError(f'Модель не выбрана {model_type}')

            return embeddings
        except Exception as err:
            raise Exception(f'Ошибка при кодировании текста: {err}')

    def search(
            self,
            query: str,
            model_type: EmbedModelType,
            collection_name: str,
            topk: int = 10,
            filter_options: dict = None,
            score_threshold: float = 0.0
        ):
        try:
            embedding = self.encode(query, model_type=model_type)
            results = self._client.search(
                collection_name=collection_name,
                query_vector=(model_type.value, embedding),
                with_payload=True,
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
        except Exception as error:
            raise Exception(f'Ошибка при поиске: {error}')

    def create_database(self, 
                        dense_embeddings: list, 
                        late_interaction_embeddings: list, 
                        collection_name: str='advisor_db'):
        """ Create the database """
        try:
            if self._client.collection_exists(collection_name=collection_name):
                return

            self._client.create_collection(
                collection_name=collection_name,
                vectors_config={

                    "all-MiniLM-L6-v2":models.VectorParams(
                        size=len(dense_embeddings[EmbedModelType.MiniLM]),
                        distance=models.Distance.COSINE
                    ),

                    "colbertv2.0": models.VectorParams(
                        size=len(late_interaction_embeddings[0][0]),
                        distance=models.Distance.COSINE,
                        multivector_config=models.MultiVectorConfig(
                            comparator=models.MultiVectorComparator.MAX_SIM,
                            )
                        ),
                    "deepvk/USER-bge-m3":models.VectorParams(
                        size=len(dense_embeddings[EmbedModelType.DEEPVK_USER]),
                        distance=models.Distance.COSINE
                    ),
                    "cointegrated/rubert-tiny2":models.VectorParams(
                        size=len(dense_embeddings[EmbedModelType.RUBERT_TINY2]),
                        distance=models.Distance.COSINE
                    ),
                    "Tochka-AI/ruRoPEBert-e5-base-2k":models.VectorParams(
                        size=len(dense_embeddings[EmbedModelType.TOCHKA]),
                        distance=models.Distance.COSINE
                    ),
                    'intfloat/multilingual-e5-large':models.VectorParams(
                        size=len(dense_embeddings[EmbedModelType.E5_LARGE]),
                        distance=models.Distance.COSINE
                    ),

                },
                sparse_vectors_config={
                    "bm25": models.SparseVectorParams(
                    modifier=models.Modifier.IDF,
                    )
                }
            )
        except Exception as error:
            raise Exception(f'Ошибка при создании базы: {error}')

    def delete_database(self, collection_name: str):
        """ Delete the database """
        try:
            self._client.delete_collection(collection_name=collection_name)
        except Exception as error:
            raise Exception(f'Ошибка при удалении базы: {error}')

    def upload_db(self, collection_name: str, batch_size: int=4):
        """ Загружаем данные в базу """

        files = self.get_all_files()
        df = self.combined_df(files).reset_index()
        
        dataset = Dataset.from_pandas(df)
        
        dense_embedding_model_MiniLM = self._setup_model(EmbedModelType.MiniLM)
        dense_embedding_model_DEEPVK_USER = self._setup_model(EmbedModelType.DEEPVK_USER)
        dense_embedding_model_RUBERT_TINY2 = self._setup_model(EmbedModelType.RUBERT_TINY2)
        dense_embedding_model_TOCHKA = self._setup_model(EmbedModelType.TOCHKA)
        
        dense_embedding_model_E5_LARGE = self._setup_model(EmbedModelType.E5_LARGE)
        
        bm25_embedding_model = self._setup_model(EmbedModelType.BM25)
        late_interaction_embedding_model = self._setup_model(EmbedModelType.BERT)

        for batch in tqdm.tqdm(dataset.iter(batch_size=batch_size), total=len(dataset) // batch_size):
            try:
                dense_embeddings_MiniLM = list(dense_embedding_model_MiniLM.encode(batch["content"]))
                dense_embeddings_DEEPVK_USER = list(dense_embedding_model_DEEPVK_USER.encode(batch["content"]))
                dense_embeddings_RUBERT_TINY2 = list(dense_embedding_model_RUBERT_TINY2.encode(batch["content"]))
                dense_embeddings_TOCHKA = list(dense_embedding_model_TOCHKA.encode(batch["content"]))
                dense_embeddings_E5_LARGE = list(dense_embedding_model_E5_LARGE.encode(batch["content"]))
                
                bm25_embeddings = list(bm25_embedding_model.passage_embed(batch["content"]))
                late_interaction_embeddings = list(late_interaction_embedding_model.passage_embed(batch["content"]))

                self._client.upload_points(
                    collection_name=collection_name,
                    points=[
                        models.PointStruct(
                            id=int(batch["index"][i]),
                            vector={
                                "all-MiniLM-L6-v2": dense_embeddings_MiniLM[i].tolist(),
                                "deepvk/USER-bge-m3": dense_embeddings_DEEPVK_USER[i].tolist(),
                                "cointegrated/rubert-tiny2": dense_embeddings_RUBERT_TINY2[i].tolist(),

                                "Tochka-AI/ruRoPEBert-e5-base-2k": dense_embeddings_TOCHKA,
                                'intfloat/multilingual-e5-large': dense_embeddings_E5_LARGE,

                                "bm25": bm25_embeddings[i].as_object(),
                                "colbertv2.0": late_interaction_embeddings[i].tolist(),
                            },
                            payload={
                                "catalog": batch["catalog"][i],
                                "category": batch["category"][i],
                                "content": batch["content"][i],
                                "url": batch["url"][i]
                            }
                        )
                        for i, _ in enumerate(batch["index"])
                    ],
                    batch_size=batch_size,  
                )
            except Exception as error:
                raise Exception(f'Ошибка при загрузке в базу: {error}')