from langchain_mistralai import ChatMistralAI
from langchain_ollama import OllamaLLM

from agent.utils import LLMModelType
from ._base import _BaseLLM




class LlamaLLM(_BaseLLM):
    api_key = 'hIBq3oF9S5hz3YmoxEDmxK9OmZW91BSx'
    def __init__(self, name: str, model_name: str, model_type: LLMModelType) -> None:
        print(model_name)
        if LLMModelType.OLLAMA == model_type:
            llm = OllamaLLM(model=model_name)
        elif LLMModelType.MISTRAL == model_type:
            llm = ChatMistralAI(model=model_name, 
                                temperature=0.5,
                                max_retries=2,
                                api_key=LlamaLLM.api_key)
            
        super().__init__(name, llm)
