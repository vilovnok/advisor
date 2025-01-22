from langchain_ollama import OllamaLLM
from agent.utils import LlmModelType
from ._base import _BaseLLM

class LlamaLLM(_BaseLLM):
    def __init__(self, name: str, model_name: str, model_type: LlmModelType) -> None:
        llm = OllamaLLM(model=model_name)            
        super().__init__(name, llm)
