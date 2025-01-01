from langchain_ollama import OllamaLLM


from agent.utils import LlmModelType
from ._base import _BaseLLM




class LlamaLLM(_BaseLLM):
    
    def __init__(self, name: str, model_name: str, model_type: LlmModelType) -> None:
        # print(model_name)
        # if LlmModelType.OLLAMA == model_type:
        llm = OllamaLLM(model=model_name)
        # elif LlmModelType.vLLM == model_type:
        #     llm = LlmModelType.QWEN.value
            
        super().__init__(name, llm)
