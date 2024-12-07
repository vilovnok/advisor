import openai
from agent.utils import LlmModelType


class OpenAIClient:
    def __init__(self, 
                model_type: LlmModelType,
                base_url: str="http://localhost:7986"):
        

        self.base_url = base_url
        
        self.setup_model(model_type)        
        self.setup_openai() 

    def setup_openai(self):
        openai.api_key = "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"
        openai.api_base = self.base_url

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
    

    