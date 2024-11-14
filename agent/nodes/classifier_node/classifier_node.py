from typing import List

from langchain_core.output_parsers import StrOutputParser, BaseOutputParser
from langchain_core.messages import AIMessage, BaseMessage

from .prompt import CLASSIFIER_NODE_PROMPT
from agent.nodes._base import _BaseNode
from agent.llms._base import _BaseLLM
from agent.graphs.state import State


class ClassifierNode(_BaseNode):
    """
    Classifier Node to classify input query (user input) in categories.
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

        vacancy = history[-1].content
        answer = self.chain.invoke({"vacancy": vacancy})

        if self.show_logs:
            print(self.name)
            print(state.catalog_name)          
            print(f"Model answer: {answer}")
            print("----------------")

        catalog_name = answer

        return {"history": history, "catalog_name": catalog_name}
