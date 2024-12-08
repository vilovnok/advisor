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

    def setup_model(self, model_type:str):
        if model_type == LlmModelType.COTYIPE:
            model = LlmModelType.COTYIPE.value

        self.model = model

    def invoke(self, prompt:str, content:str):
        response = openai.ChatCompletion.create(
            model=self.model,
            temperature=0.2,
            frequency_penalty=0.2,
            max_tokens=2048,
            top_p=0.8,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": content}
                ]
            )
        return response["choices"][0]["message"]["content"]
    

    