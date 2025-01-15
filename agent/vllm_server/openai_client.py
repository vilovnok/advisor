import re
import openai
from agent.utils import LlmModelType, PromptSanitizer
from agent.vllm_server.utils import openai_key, api_base


class OpenAIClient(PromptSanitizer):
    def __init__(self, 
                model_type: LlmModelType=LlmModelType,
                api_key: str=openai_key,
                api_base: str=api_base):
        
        self.__setup_model(model_type)        
        self.__setup_openai(api_key=api_key, api_base=api_base) 
    def __setup_openai(self, api_key:str, api_base:str):
        openai.api_key = api_key
        openai.api_base = api_base

    def __setup_model(self, model_type:LlmModelType):
        if model_type == LlmModelType.QWEN:
            model = LlmModelType.QWEN.value

        self.model = model

    def ChatCompletion(self, prompt:str, content:str):
        formatted_user_input = self.get_completion_from_messages(input_text=content, delimiter='#'*3)    
        try:
            messages=[ 
                {"role": "system", "content": prompt}, 
                {"role": "user", "content": formatted_user_input}
            ]

            response = openai.ChatCompletion.create(
                model=self.model,
                temperature=0.2,
                frequency_penalty=0.2,
                max_tokens=1024,
                top_p=0.8,
                messages=messages
            )
            
            return self.validate_response(response["choices"][0]["message"]["content"])

        except openai.error.InvalidRequestError as e:
            print(f"Invalid request: {e}")
        except openai.error.RateLimitError as e:
            print(f"Rate limit exceeded: {e}")
        except openai.error.OpenAIError as e:
            print(f"OpenAI error: {e}")        
        except Exception as e:
            print(f"Other error occurred: {e}")

    def Completion(self, prompt:str, content:str):
        formatted_user_input = self.get_completion_from_messages(input_text=content, delimiter='#'*3)    
        prompt = prompt.replace('{context}',formatted_user_input)

        try:
            response = openai.Completion.create(
                model=self.model,
                temperature=0.0,
                prompt = prompt,
                max_tokens=1024,
            )
            return self.fix_response(response["choices"][0]["text"]) 
        except Exception as error:
            print(f"Ошибка при вызове OpenAI:\n{error}")
        except openai.error.InvalidRequestError as e:
            print(f"Invalid request: {e}")
        except openai.error.RateLimitError as e:
            print(f"Rate limit exceeded: {e}")
        except openai.error.OpenAIError as e:
            print(f"OpenAI error: {e}")        
        except Exception as e:
            print(f"Other error occurred: {e}")

    def invoke(self, prompt: str, content:str):
        try:
            
            response = openai.ChatCompletion.create(
                model=self.model,
                temperature=0.2,
                frequency_penalty=0.2,
                max_tokens=784,
                top_p=0.8,
                messages=[
                    {"role": "system", "content": f'{prompt}'},
                    {"role": "user", "content": f'{content}'}
                    ]
                )
            return response["choices"][0]["message"]["content"]
        except Exception as error:
            print(f"Ошибка при вызове OpenAI:\n{error}")