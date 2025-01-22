from langchain_core.output_parsers import BaseOutputParser
from langchain_core.messages import FunctionMessage

from agent.database import Retriever
from agent.nodes._base import _BaseNode
from agent.llms._base import _BaseLLM
from agent.graphs.state import State

from agent.utils import EmbedModelType


class RetrieverNode(_BaseNode):
    """
    Retriever Node to pull relevant information based on user input.
    """
    DATABASE_COLLECTION_NAME = "advisor_last_db"

    def __init__(
            self,
            name: str,
            description: str,
            llm: _BaseLLM = None,
            prompt: str = None,
            output_parser: BaseOutputParser = None,
            show_logs: bool = False,
            retriever: Retriever = None,
            score_threshold: float = 0.0,
            topK: int = 10,
        ) -> None:
        self.name = name
        self.description = description
        self.score_threshold = score_threshold
        self.topK = topK
        self.show_logs = show_logs
        self.retriever = Retriever(device=0) if not retriever else retriever

    def invoke(self, state: State):
        history = state.history
        activity_name = state.activity_name  
        category_name = 'cv' if state.category_name=='vac' else 'cv'
    
        # retrieved_info = self.retriever.search(
        #     query=history[-1].content,
        #     collection_name=RetrieverNode.DATABASE_COLLECTION_NAME,
        #     filter_options={"catalog": category_name, 'category': activity_name},
        #     topk=self.topK,
        #     score_threshold=self.score_threshold, 
        #     model_type=EmbedModelType.DEEPVK_USER
        # )

        retrieved_info = self.retriever.hybrid_search(
            query=history[-1].content,
            collection_name=RetrieverNode.DATABASE_COLLECTION_NAME,
            # filter_options={"catalog": category_name},
            filter_options={"catalog": category_name, 'category': activity_name},
        )
        
        examples = "\n\n".join([f'id: {item.id}\n{item.payload["content"]}' for item in retrieved_info.points])
        if self.show_logs:
            print(self.name)          
            print(f'activity_name: {state.activity_name}\ncategory_name: {category_name}')
            for i in [item.payload["content"] for item in retrieved_info.points]:
                print('\n\n')
                print(i)
                print('\n\n')
            print("----------------")

        history.append(FunctionMessage(name="RetrieverNode", content=examples))

        return {"history": history, "activity_name": state.activity_name, "category_name": category_name}