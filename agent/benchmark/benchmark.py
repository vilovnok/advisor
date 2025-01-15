import pandas as pd
from typing import List
from ranx import evaluate as eval
from qdrant_client import QdrantClient, models
from fastembed.sparse.bm25 import Bm25
from fastembed.embedding import TextEmbedding
from sentence_transformers import SentenceTransformer
from fastembed.late_interaction import LateInteractionTextEmbedding

from agent.utils import EmbedModelType


class Benchmark:
    """
    Класс для гибридного поиска и оценки качества ранжирования.
    """

    def __init__(
        self,
        collection_name: str = 'advisor_db',
        url: str = "http://localhost:6333",
    ):
        self.collection_name = collection_name
        
        self._setup_database(url=url, collection_name=collection_name)
        self._setup_encoders()

    def _setup_database(self, url: str = None, collection_name: str = None):
        """
        Настраивает подключение к Qdrant.

        Args:
            url (str): URL адрес базы данных Qdrant.
            collection_name (str): Название коллекции.
        """
        self.client = QdrantClient(f'{url}')
        if not self.client.collection_exists(collection_name):
            raise ValueError(f"Collection {collection_name} does not exist!")

    def _setup_encoders(self):
        """
        Инициализирует модели для эмбеддингов.
        """
        self.dense_embedding_model_MiniLM = TextEmbedding(
            EmbedModelType.MiniLM.value
        )
        self.dense_embedding_model_DEEPVK_USER = SentenceTransformer(
            EmbedModelType.DEEPVK_USER.value
        )
        self.dense_embedding_model_RUBERT_TINY2 = SentenceTransformer(
            EmbedModelType.RUBERT_TINY2.value
        )
        self.dense_embedding_model_TOCHKA = SentenceTransformer(
            EmbedModelType.TOCHKA.value
        )
        self.dense_embedding_model_E5_LARGE = SentenceTransformer(
            EmbedModelType.E5_LARGE.value
        )
        self.bm25_embedding_model = Bm25(EmbedModelType.BM25.value)

        self.late_interaction_embedding_model = LateInteractionTextEmbedding(
            EmbedModelType.BERT.value
        )

    def create_prefetch_from_models(
        self,
        query: str,
        models_list: List[str],
        limit: int,
        topK: int,
    ) -> List[models.Prefetch]:
        """
        Создает список Prefetch для гибридного поиска.

        Args:
            query (str): Текст запроса.
            models_list (List[str]): Список моделей.
            limit (int): Ограничение результатов.

        Returns:
            List[models.Prefetch]: Список объектов Prefetch.
        """
        prefetch = []

        for model_name in models_list:
            if model_name == "all-MiniLM-L6-v2":
                prefetch.append(
                    models.Prefetch(
                        query=next(self.dense_embedding_model_MiniLM.query_embed(query)),
                        using="all-MiniLM-L6-v2",
                        limit=limit,
                    )
                )
            elif model_name == "bm25":
                prefetch.append(
                    models.Prefetch(
                        query=models.SparseVector(
                            **next(self.bm25_embedding_model.query_embed(query)).as_object()
                        ),
                        using="bm25",
                        limit=limit,
                    )
                )
            elif model_name == "colbertv2.0":
                prefetch.append(
                    models.Prefetch(
                        query=next(self.late_interaction_embedding_model.query_embed(query)),
                        using="colbertv2.0",
                        limit=limit,
                    )
                )
            elif model_name == "deepvk/USER-bge-m3":
                prefetch.append(
                    models.Prefetch(
                        query=self.dense_embedding_model_DEEPVK_USER.encode(
                            query, normalize_embeddings=True
                        ),
                        using="deepvk/USER-bge-m3",
                        limit=limit,
                    )
                )
            elif model_name == "cointegrated/rubert-tiny2":
                prefetch.append(
                    models.Prefetch(
                        query=self.dense_embedding_model_RUBERT_TINY2.encode(
                            query, normalize_embeddings=True
                        ),
                        using="cointegrated/rubert-tiny2",
                        limit=limit,
                    )
                )
            elif model_name == "Tochka-AI/ruRoPEBert-e5-base-2k":
                prefetch.append(
                    models.Prefetch(
                        query=self.dense_embedding_model_TOCHKA.encode(
                            query, normalize_embeddings=True
                        ),
                        using="Tochka-AI/ruRoPEBert-e5-base-2k",
                        limit=limit,
                    )
                )
            elif model_name == 'intfloat/multilingual-e5-large':
                prefetch.append(
                    models.Prefetch(
                        query=self.dense_embedding_model_E5_LARGE.encode(
                            query, normalize_embeddings=True
                        ),
                        using='intfloat/multilingual-e5-large',
                        limit=limit,
                    )
                )
            elif model_name == 'intfloat/multilingual-e5-large+bm25':
                prefetch.append(
                    models.Prefetch(
                        query=self.dense_embedding_model_E5_LARGE.encode(
                            query, normalize_embeddings=True
                        ),
                        using='intfloat/multilingual-e5-large',
                        limit=limit
                    )
                )
            elif model_name == 'Tochka-AI/ruRoPEBert-e5-base-2k+bm25':
                prefetch.append(
                    models.Prefetch(
                        prefetch=[
                            models.Prefetch(
                        query=self.dense_embedding_model_TOCHKA.encode(
                            query, normalize_embeddings=True
                        ),
                        using='Tochka-AI/ruRoPEBert-e5-base-2k',
                        limit=limit
                            )],
                        query=models.SparseVector(
                            **next(self.bm25_embedding_model.query_embed(query)).as_object()
                        ),
                        using="bm25",
                        limit=limit,
                    )
                )
            elif model_name == 'deepvk/USER-bge-m3+bm25':
                                prefetch.append(
                    models.Prefetch(
                        prefetch=[
                            models.Prefetch(
                        query=self.dense_embedding_model_DEEPVK_USER.encode(
                            query, normalize_embeddings=True
                        ),
                        using='deepvk/USER-bge-m3',
                        limit=limit
                            )],
                        query=models.SparseVector(
                            **next(self.bm25_embedding_model.query_embed(query)).as_object()
                        ),
                        using="bm25",
                        limit=limit,
                    )
                )
            elif model_name == 'all-MiniLM-L6-v2+bm25':
                prefetch.append(
                    models.Prefetch(
                        prefetch=[
                            models.Prefetch(
                        query=next(self.dense_embedding_model_MiniLM.query_embed(query)),
                        using='all-MiniLM-L6-v2',
                        limit=limit
                            )],
                        query=models.SparseVector(
                            **next(self.bm25_embedding_model.query_embed(query)).as_object()
                        ),
                        using="bm25",
                        limit=limit,
                    )
                )
            elif model_name == "cointegrated/rubert-tiny2+bm25":
                prefetch.append(
                    models.Prefetch(
                        prefetch=[
                            models.Prefetch(
                        query=self.dense_embedding_model_RUBERT_TINY2.encode(
                            query, normalize_embeddings=True
                        ),
                        using="cointegrated/rubert-tiny2",
                        limit=limit
                            )],
                        query=models.SparseVector(
                            **next(self.bm25_embedding_model.query_embed(query)).as_object()
                        ),
                        using="bm25",
                        limit=limit,
                    )
                )
            
            else:
                raise ValueError(f"Unknown model: {model_name}")

        return prefetch

    def hybrid_query_dynamic(
        self,
        collection_name: str,
        query: str,
        models_list: List[str],
        limit: int = 10,
        topK: int = 10,
        filter_options: dict = None,
    ):
        """
        Выполняет гибридный запрос с динамическим Prefetch.

        Args:
            collection_name (str): Название коллекции.
            query (str): Текст запроса.
            models_list (List[str]): Список моделей.
            limit (int): Ограничение результатов.
            filter_options (dict): Дополнительные фильтры.

        Returns:
            Any: Результаты запроса.
        """
        try:
            prefetch = self.create_prefetch_from_models(
                query=query, models_list=models_list, limit=limit, topK=topK
            )
            response = self.client.query_points(
                collection_name=collection_name,
                prefetch=prefetch,
                query=models.FusionQuery(fusion=models.Fusion.RRF),
                with_payload=True,
                limit=limit,
                query_filter=models.Filter(
                    must=[
                        models.FieldCondition(key=k, match=models.MatchValue(value=v))
                        for k, v in filter_options.items()
                    ]
                ) if filter_options else None,
            )
            return response
        except Exception as e:
            raise ValueError(f"Error during query: {e}")

    def evaluate_ranking(
        self,
        ground_truth: str,
        result,
        topK: int = 10,
    ):
        """
        Оценивает качество ранжирования.

        Args:
            ground_truth (str): Истинное значение.
            result: Результаты запроса.
            limit (int): Ограничение на количество результатов.

        Returns:
            dict: Метрики качества ранжирования.
        """
        try:
            points = result.points
            if not points:
                raise ValueError("No points returned from the query.")

            targets = {
                f"doc_{point.id}": 1 if f"{point.payload['catalog']}-{point.payload['category']}" == ground_truth else 0
                for point in points
            }

            qrels = {"query_1": targets}
            run = {"query_1": {f"doc_{point.id}": point.score for point in points}}

            ranking_assessment = eval(
                qrels,
                run,
                metrics=[
                    "ndcg", f"precision@{topK}", f"map@{topK}",
                    f"recall@{topK}", f"mrr@{topK}", f"dcg@{topK}"
                ],
                make_comparable=True,
            )
            return ranking_assessment
        except Exception as e:
            raise ValueError(f"Error during evaluation: {e}")

    def evaluate(self, 
            query_text: str,
            models_list:list,
            ground_truth: str,
            topK:int=10,
            limit:int=20,
            filter_options: dict=None,
        ):
            response = self.hybrid_query_dynamic(collection_name=self.collection_name, 
                            query=query_text, 
                            models_list=models_list, 
                            limit=limit,
                            topK=topK, 
                            filter_options=filter_options)

            # response = self.hybrid_query_dynamic_debug(collection_name=self.collection_name, 
            #                 query=query_text, 
            #                 models_list=models_list, 
            #                 limit=limit, 
            #                 filter_options=filter_options)
                    
            metrics = self.evaluate_ranking(ground_truth=ground_truth, 
                                    result=response, topK=topK)

            return metrics


    def benchmark(
        self,
        models: list[list[str]],
        ground_truth: str,
        query_text: str,
        topK: int=10,
        limit: int = 20,
        filter_options: dict = None,
    ):
        """
        Генерирует таблицу метрик для групп моделей.

        Args:
            models (list): Список моделей.
            ground_truth (str): Истинное значение.
            query_text (str): Текст запроса.
            limit (int): Ограничение на количество результатов.

        Returns:
            pd.DataFrame: Таблица с метриками.
        """
        scores = []

        for model in models:
            try:
                metrics = self.evaluate(
                    topK=topK,
                    limit=limit,
                    models_list=model,
                    ground_truth=ground_truth,
                    query_text=query_text,
                    filter_options=filter_options,
                )
                scores.append({"models": ", ".join(model), **metrics})
            except Exception as e:
                raise ValueError(f"Error evaluating models {model}: {e}")

        metrics_table = pd.DataFrame(scores)
        metrics_table = metrics_table[["models"] + [col for col in metrics_table.columns if col != "models"]]

        return metrics_table
