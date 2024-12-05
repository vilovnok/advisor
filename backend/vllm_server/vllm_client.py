import openai
import requests


class VLLMClient:
    def __init__(self, 
                model: str=None,
                base_url: str="http://localhost:7986"):
        """
        Инициализация клиента для работы с vLLM сервером.
        """
        self.base_url = base_url
        self.model = model
        
        self.health_check()
        self.setup_openai()

    def setup_openai(self):
        openai.api_key = "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"
        openai.api_base = self.base_url

    def health_check(self):
        """Проверяет состояние сервера."""
        response = requests.get(f"{self.base_url}/health")
        if response.status_code == 200:
            return {"status": "ok", "details": response.headers}
        else:
            response.raise_for_status()

    def list_models(self):
        """Возвращает список доступных моделей."""
        response = requests.get(f"{self.base_url}/v1/models")
        response.raise_for_status()
        return response.json()

    def create_completion(self, 
                          prompt: list, 
                          max_tokens: int = 512, 
                          **kwargs
    ):
        """
        Создает текстовую комплитацию.

        :param model: Имя модели.
        :param prompt: Входной текст.
        :param max_tokens: Максимальное количество токенов в ответе.
        :param kwargs: Дополнительные параметры (temperature, top_p и т.д.).
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            **kwargs,
        }

        response = requests.post(f"{self.base_url}/v1/completions", json=payload)
        response.raise_for_status()
        return response.json()

    def create_chat_completion(self, 
                               messages: list, 
                               max_tokens: int = 256, 
                               **kwargs
    ):
        """
        Создает чат-комплитацию.

        :param model: Имя модели.
        :param messages: Список сообщений чата.
        :param max_tokens: Максимальное количество токенов в ответе.
        :param kwargs: Дополнительные параметры (temperature, top_p и т.д.).
        """
        payload = {
            "model": self.model,
            # "messages": messages,
            "max_tokens": max_tokens,
            **kwargs
        },

        response = requests.post(f"{self.base_url}/v1/chat/completions", json=payload)
        response.raise_for_status()
        return response.json()

    def generate_embeddings(self, 
                            model: str, 
                            input_texts: list,
                            encoding_format: str,
                            dimensions: int,
                            user: str,
                            truncate_prompt_tokens: bool,
                            additional_data: dict,
                            add_special_tokens: bool,
                            priority: int):    
        """
        Генерирует эмбеддинги для заданного текста.

        :param model: Имя модели.
        :param input_texts: Список текстов.
        """
        payload = {
            "model": model,
            "input": input_texts,
            "encoding_format": encoding_format,
            "dimensions": dimensions,
            "user": user,
            "truncate_prompt_tokens": truncate_prompt_tokens,
            "additional_data": additional_data,
            "add_special_tokens": add_special_tokens,
            "priority": priority
        }
        response = requests.post(f"{self.base_url}/v1/embeddings", json=payload)
        response.raise_for_status()
        return response.json()

    def tokenize(self, text: str):
        """Токенизирует текст."""
        payload = {
                    "model": self.model,
                    "prompt": text,
                    "add_special_tokens": True
                    }
        
        response = requests.post(f"{self.base_url}/tokenize", json=payload)
        response.raise_for_status()
        return response.json()

    def detokenize(self, tokens: list):
        """Объединяет токены обратно в текст."""
        payload = {
                    "model": self.model,
                    "tokens": tokens
                    }
        response = requests.post(f"{self.base_url}/detokenize", json=payload)
        response.raise_for_status()
        return response.json()
    



# # 6. Токенизация
# tokens = client.tokenize("Пример текста.")
# print(tokens)

# # # 7. Декодинг токенов
# text = client.detokenize(tokens["tokens"])
# print(text)