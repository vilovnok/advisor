from typing import Dict, List
from abc import ABC

from langchain_core.output_parsers import StrOutputParser, BaseOutputParser
from langchain_core.messages import FunctionMessage, BaseMessage
from langchain_core.prompts import PromptTemplate

from agent.llms._base import _BaseLLM
from agent.graphs.state import State
from agent.vllm_server.openai_client import OpenAIClient
from agent.utils import LlmModelType


class _BaseNode(ABC):
    def __init__(
            self,
            name: str,
            description: str,
            llm: _BaseLLM,
            prompt: list[str] | str = "",
            output_parser: BaseOutputParser = StrOutputParser(),
        ) -> None:
        self.name = name
        self.description = description
        self.chain = PromptTemplate.from_template(prompt) | llm.llm | output_parser
        self.vllm = VLLMAdapter(prompt=prompt)

    def get_summary(self, history: List[BaseMessage]):
        print(f'History::: {history}')
        for replic in history[::-1]:
            if isinstance(replic, FunctionMessage) and replic.name == "SummarizationNode":
                return replic.content
        raise Exception("Not found summary")


class _BaseRouter(ABC):
    def __init__(
            self,
            name: str,
            description: str,
            mapping: Dict,
        ) -> None:
        self.name = name
        self.description = description
        self._mapping = mapping

    @property
    def mapping(self):
        return self._mapping

    def invoke(self, state: State):
        pass


class VLLMAdapter(ABC):
    def __init__(self, prompt:str):
        self.prompt = prompt

        self._setupVLLM()

    def _setupVLLM(self):            
        self.vllm_client = OpenAIClient(model_type=LlmModelType.QWEN)        
    
    def ChatCompletion(self, content: str):
        response = self.vllm_client.ChatCompletion(prompt=self.prompt, content=content)
        return response
    
    def Completion(self, content: str, prompt:str=None,):
        if not prompt:
            prompt = self.prompt
        response = self.vllm_client.Completion(prompt=prompt, content=content)
        return response