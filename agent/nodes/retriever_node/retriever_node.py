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
    DATABASE_COLLECTION_NAME = "advisor_db"

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
        category_name = state.category_name        
    
        retrieved_info = self.retriever.search(
            query=history[-1].content,
            collection_name=RetrieverNode.DATABASE_COLLECTION_NAME,
            filter_options={"catalog": state.catalog_name, 'category': category_name},
            topk=self.topK,
            score_threshold=self.score_threshold, 
            model_type=EmbedModelType.DEEPVK_USER
        )
        
        examples = "\n\n".join([f'id: {item.id}\n{item.payload["content"]}' for item in retrieved_info])
        if self.show_logs:
            print(self.name)          
            print(f'catalog_name: {state.catalog_name}\ncategory_name: {category_name}')
            # for i in [item.payload["content"] for item in retrieved_info]:
            #     print('\n\n')
            #     print(i)
            #     print('\n\n')
            print("----------------")

        history.append(FunctionMessage(name="RetrieverNode", content=examples))

        return {"history": history, "catalog_name": state.catalog_name, "category_name": category_name}