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
    def __init__(
            self,
            collection_name: str='advisor_db',
            url: str="http://localhost:6333",
    ):
        self._setup_database(url=url, collection_name=collection_name)
        self._setup_encoders()


    def _setup_database(self, url:str=None, collection_name:str=None):
        self.client = QdrantClient(f'{url}')
        if not self.client.collection_exists(collection_name):
            raise ValueError("Collection %s is not exists!" % collection_name)

    def _setup_encoders(self):
        self.dense_embedding_model_MiniLM = TextEmbedding(EmbedModelType.MiniLM.value)
        self.dense_embedding_model_DEEPVK_USER = SentenceTransformer(EmbedModelType.DEEPVK_USER.value)
        self.bm25_embedding_model = Bm25(EmbedModelType.BM25.value)
        self.late_interaction_embedding_model = LateInteractionTextEmbedding(EmbedModelType.BERT.value)        

    def create_prefetch_from_models(self, query: str, models_list: List[str], limit: int) -> List[models.Prefetch]:
        """
        Создает список Prefetch для гибридного поиска на основе списка моделей.

        Args:
            query (str): Текст запроса.
            models_list (List[str]): Список строковых названий моделей.
            limit (int): Максимальное количество результатов на запрос.

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
                        query=models.SparseVector(**next(self.bm25_embedding_model.query_embed(query)).as_object()),
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
                        query=self.dense_embedding_model_DEEPVK_USER.encode(query, normalize_embeddings=True),
                        using="deepvk/USER-bge-m3",
                        limit=limit,
                    )
                )
            else:
                raise ValueError(f"Неизвестная модель: {model_name}")

        return prefetch


    def hybrid_query_dynamic(
            self,
            collection_name: str,         
            query: str, 
            models_list: List[str], 
            limit: int=10,
            filter_options: dict=None):
        """
        Выполняет гибридный запрос с использованием динамического создания Prefetch.

        Args:
            collection_name (str): Название коллекции в базе.
            query (str): Текст запроса.
            models_list (List[str]): Список названий моделей для Prefetch.
            limit (int): Максимальное количество результатов.

        Returns:
            Any: Результаты запроса.
        """
        
        try:
            prefetch = self.create_prefetch_from_models(query=query, models_list=models_list, limit=limit)
            response = self.client.query_points(
                collection_name=collection_name,
                prefetch=prefetch,
                query=models.FusionQuery(
                    fusion=models.Fusion.RRF,
                ),
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
            raise ValueError(f"Error during evaluation: {e}")

    def evaluate_ranking(self, 
                        ground_truth:str, 
                        result, 
                        limit:int=10):
        try:        
            points = result.points
            if not points:
                raise ValueError("No points returned from the query.")

            targets = {}
            for point in points:
                catalog = point.payload['catalog']
                category = point.payload['category']
                similar = f"{catalog}-{category}"

                target = 1 if similar == ground_truth else 0
                targets[f"doc_{point.id}"] = target

            qrels = {"query_1": targets}
            run = {"query_1": {f"doc_{point.id}": point.score for point in points}}
            
            ranking_assessment = eval(
                qrels, 
                run, 
                metrics=["ndcg", f"precision@{limit}", f"map@{limit}", 
                        f"recall@{limit}", f"mrr@{limit}", f"dcg@{limit}"], 
                make_comparable=True
            )
            
            return ranking_assessment
        except Exception as e:
            raise ValueError(f"Error during evaluation: {e}")

        
    def evaluate(self, 
            query_text: str,
            models_list:list,
            ground_truth: str,
            limit:int=10,
            filter_options: dict=None,
        ):
            response = self.hybrid_query_dynamic(collection_name='advisor_db', 
                            query=query_text, 
                            models_list=models_list, 
                            limit=limit, 
                            filter_options=filter_options)
                    
            metrics = self.evaluate_ranking(ground_truth=ground_truth, 
                                    result=response, limit=limit)

            return metrics
    
    def benchmark(self, 
        models:list, 
        ground_truth:str, 
        query_text:str, 
        limit=10,
        filter_options: dict=None,
        ):
        """
        Генерирует таблицу метрик для списка групп моделей.

        Args:
            client: Объект клиента с методом evaluate.
            models_lists (list): Список групп моделей для оценки.
            ground_truth (str): Истинные данные для оценки.
            query_text (str): Текст запроса.
            limit (int): Ограничение на количество результатов (по умолчанию 10).

        Returns:
            pd.DataFrame: Таблица метрик для каждой группы моделей.
        """

        scorse = []
        for model in models:
            try:
                metrics = self.evaluate(
                    limit=limit,
                    models_list=model,
                    ground_truth=ground_truth,
                    query_text=query_text,
                    filter_options=filter_options
                )            
                scorse.append({"models": ", ".join(model), **metrics})
            except Exception as e:
                raise ValueError(f"Ошибка при оценке для моделей {model}: {e}")
        
        metrics_table = pd.DataFrame(scorse)
        metrics_table = metrics_table[["models"] + [col for col in metrics_table.columns if col != "models"]]
    
        return metrics_table


    # def benchmark(self, 
    #         query_text: str,
    #         models_lists:list,
    #         ground_truth: str,
    #         limit:int=10,
    #         filter_options: dict=None,
    #     ):

    #     # benchmark = dict()
    #     qrels = None
    #     benchmark = {"qrels": [], "runs": []}

    #     for idx, models_list in enumerate(models_lists):

    #         result = self.hybrid_query_dynamic(
    #             collection_name='advisor_db', 
    #             query=query_text, 
    #             models_list=models_list, 
    #             limit=limit, 
    #             filter_options=filter_options
    #         )

    #         try:
    #             current_qrels, current_run = self.evaluate_ranking(
    #                 ground_truth=ground_truth, 
    #                 result=result, 
    #                 limit=limit, 
    #                 table=True
    #             )
    #         except Exception as e:
    #             print(f"Error during evaluation for models {models_list}: {e}")
    #             continue

    #         if not current_qrels or not current_run:
    #             print(f"Skipping models {models_list}: Empty qrels or run.")
    #             continue

    #         if qrels is None:
    #             qrels = current_qrels
    #         elif qrels != current_qrels:
    #             print(f"Warning: Несогласованные qrels для моделей {models_list}. Пропускаем эти данные.")
    #             continue


    #         model_name = "-".join(models_list)
            

    #         benchmark['qrels'].append(current_qrels)
    #         benchmark['runs'].append(Run(current_run, name=f"{model_name}"))
        
    #     if not benchmark["runs"]:
    #         raise ValueError("Не удалось собрать данные для сравнения моделей.")

    #     metrics_comparison = self.compare_models(
    #         qrels=benchmark['qrels'][0],
    #         runs=benchmark['runs'],
    #         metrics=["precision@10", "recall@10", "mrr@10", "dcg@10", "ndcg@10"],
    #     )

    #     print("Comparison Results:", metrics_comparison)
    #     return metrics_comparison


    # def compare_models(
    #         self,
    #         qrels: dict,
    #         runs: list,
    #         metrics: list = None
    #     ) -> dict:
    #     """
    #     Сравнивает метрики для разных моделей с использованием `ranx.compare`.

    #     Args:
    #         qrels (dict): Релевантность (qrels) в формате, ожидаемом ranx.
    #         runs (list): Список ранжированных результатов от различных моделей.
    #         metrics (list): Список метрик для сравнения. По умолчанию включает стандартные метрики.

    #     Returns:
    #         dict: Результаты сравнения метрик для разных моделей.
    #     """
    #     if metrics is None:
    #         metrics = ["precision@10", "recall@10", "mrr@10", "dcg@10", "ndcg@10"]

    #     try:
    #         results = compare(
    #             qrels=qrels,
    #             runs=runs,
    #             metrics=metrics
    #         )
    #         return results
    #     except Exception as e:
    #         raise ValueError(f"Ошибка при сравнении метрик: {e}")
        

    # def table_evaluate_ranking(self, 
    #                     ground_truth:str, 
    #                     result, 
    #                     limit:int=2,
    #                     table:bool=False):
    #     try:        
    #         points = result.points
    #         if not points:
    #             raise ValueError("No points returned from the query.")

    #         targets = {}
    #         for point in points:
    #             catalog = point.payload['catalog']
    #             category = point.payload['category']
    #             similar = f"{catalog}-{category}"

    #             target = 1 if similar == ground_truth else 0
    #             targets[f"doc_{point.id}"] = target

    #         qrels = {"query_1": targets}
    #         run = {"query_1": {f"doc_{point.id}": point.score for point in points}}
    #         if not table:
    #             ranking_assessment = eval(
    #                 qrels, 
    #                 run, 
    #                 metrics=["ndcg", f"precision@{limit}", f"map@{limit}"], 
    #                 make_comparable=True
    #             )
                
    #             return ranking_assessment
    #         return zip(qrels, run)

    #     except Exception as e:
    #         raise ValueError(f"Error during evaluation: {e}")  