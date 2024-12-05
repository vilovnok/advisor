import openai
from .request import VLLMClient


client = VLLMClient(base_url="http://localhost:7986")

# print(client.health_check())

# print(client.list_models())

# 5. Генерация эмбеддингов
embeddings = client.generate_embeddings(
    model="meta-llama/Llama-2-7b-hf",
    input_texts=["Пример текста для эмбеддингов."],
    encoding_format="float",
    dimensions=512,
    user="r1char9",
    truncate_prompt_tokens=1,
    additional_data=None,
    add_special_tokens=True,
    priority=1
)
print(embeddings)

# # 6. Токенизация
# tokens = client.tokenize("Пример текста")
# print(tokens)

# # 7. Декодинг токенов
# text = client.detokenize(tokens["tokens"])
# print(text)








# completion = client.create_completion(
#     model="meta-llama/Llama-2-7b-hf",
#     prompt="Привет, как дела?",
#     max_tokens=50,
#     temperature=0.7
# )
# print(completion)

# chat_response = client.create_chat_completion(
#     model="meta-llama/Llama-2-7b-hf",
#     messages=[
#         {"role": "system", "content": "Ты добрый помощник."},
#         {"role": "user", "content": "Как дела?"}
#     ],
#     max_tokens=50,
#     temperature=0.9
# )
# print(chat_response)




import requests

class VLLMClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def health_check(self):
        try:
            response = requests.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"status": "error", "details": str(e)}

    def get_embeddings(self, model, input_data, encoding_format, dimensions, user, truncate_prompt_tokens, additional_data, add_special_tokens, priority):
        url = f"{self.base_url}/v1/embeddings"
        payload = {
            "model": model,
            "input": input_data,
            "encoding_format": encoding_format,
            "dimensions": dimensions,
            "user": user,
            "truncate_prompt_tokens": truncate_prompt_tokens,
            "additional_data": additional_data,
            "add_special_tokens": add_special_tokens,
            "priority": priority
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()  # Возвращает декодированный JSON
        except requests.RequestException as e:
            return {"status": "error", "details": str(e)}