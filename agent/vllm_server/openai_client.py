import openai
from agent.utils import LlmModelType


class OpenAIClient:
    def __init__(self, 
                model_type: LlmModelType,
                api_key: str,
                api_base: str="http://localhost:7986"):
        
        self.setup_model(model_type)        
        self.setup_openai(api_key=api_key, api_base=api_base) 

    def setup_openai(self, api_key:str, api_base:str):
        openai.api_key = api_key
        openai.api_base = api_base

    def setup_model(self, model_type:LlmModelType):
        if model_type == LlmModelType.COTYIPE:
            model = LlmModelType.COTYIPE.value
        elif model_type == LlmModelType.QWEN:
            model = LlmModelType.QWEN.value

        self.model = model

    def invoke(self, prompt:str, content:str):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                temperature=0.2,
                frequency_penalty=0.2,
                max_tokens=1024,
                top_p=0.8,
                messages=[
                    {"role": "system", "content": f'{prompt}'},
                    {"role": "user", "content": f'{content}'}
                    ]
                )
            return response["choices"][0]["message"]["content"]
        except Exception as error:
            print(f"Ошибка при вызове OpenAI:\n{error}")
    

    