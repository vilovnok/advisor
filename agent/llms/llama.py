from langchain_mistralai import ChatMistralAI
from langchain_ollama import OllamaLLM

from agent.utils import LlmModelType
from ._base import _BaseLLM




class LlamaLLM(_BaseLLM):
    api_key = 'hIBq3oF9S5hz3YmoxEDmxK9OmZW91BSx'
    def __init__(self, name: str, model_name: str, model_type: LlmModelType) -> None:
        print(model_name)
        if LlmModelType.OLLAMA == model_type:
            llm = OllamaLLM(model=model_name)
        elif LlmModelType.vLLM == model_type:
            llm = 
            
        super().__init__(name, llm)
