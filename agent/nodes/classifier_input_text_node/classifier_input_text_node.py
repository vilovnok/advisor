from typing import List

from langchain_core.output_parsers import StrOutputParser, BaseOutputParser

from .prompt import CLASSIFIER_NODE_PROMPT
from agent.nodes._base import _BaseNode
from agent.llms._base import _BaseLLM
from agent.graphs.state import State




class ClassifierInputTextNode(_BaseNode):
    """
    Classifier Text Node to classify input query (user input) in categories.
    """
    def __init__(
            self,
            name: str,
            description: str,
            llm: _BaseLLM,
            prompt: str = CLASSIFIER_NODE_PROMPT,
            output_parser: BaseOutputParser = StrOutputParser(),
            show_logs: bool = False
        ) -> None:
        super().__init__(name, description, llm, prompt, output_parser)
        self.show_logs = show_logs
        
    def invoke(self, state: State):
        history = state.history
        content = history[-1].content
    
        # catalog_name = self.vllm.invoke(content=content)

        # if 'вакансия' in catalog_name.lower():
        #     catalog_name = 'vac'
        # elif 'резюме' in catalog_name.lower():
        #     catalog_name = 'cv'
        # else:
        #     catalog_name = state.catalog_name

        if self.show_logs:
            print(self.name)            
            print(f"Model answer: {state.catalog_name}")
            print("----------------")        

        return {"history": history, "catalog_name": state.catalog_name, 'category_name': state.category_name}
