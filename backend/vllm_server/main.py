import openai

def setup_openai():
    openai.api_key = "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"
    openai.api_base = "http://localhost:7986"

setup_openai()

system_prompt = "Ты бот который отвечает очень грубо"
user_prompt = "Как дела?"

messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

result = openai.ChatCompletion.create(
            model="meta-llama/Llama-2-7b-hf",
            messages=messages,
            max_tokens=4096,
            temperature=0.9,
            top_p=0.6
        )
print(result["choices"][0].get("message").get("content"))




# from .vllm_client import VLLMClient


# client = VLLMClient(base_url="http://localhost:7986")
# info_model = client.list_models()
# model = info_model['data'][0]['id']

# client = VLLMClient(base_url="http://localhost:7986", model=model)

# Генерация эмбеддингов
# embeddings = client.generate_embeddings(
#     model="meta-llama/Llama-2-7b-hf",
#     input_texts=["Пример текста для эмбеддингов."],
#     encoding_format="float",
#     dimensions=512,
#     user="r1char9",
#     truncate_prompt_tokens=1,
#     additional_data=None,
#     add_special_tokens=True,
#     priority=1
# )
# print(embeddings)




# completion = client.create_completion(
#     prompt=["Расскажи историю"],
#     max_tokens=1024,
#     temperature=0.2
# )
# print(completion['choices'][0]['text'])


# messages=[
#                 {
#                     "role": "system", 
#                     "content": "You are a helpful assistant.",
#                     "name": "bot"
#                 },
#                 {
#                     "role": "user", 
#                     "content": "Расскажи мне тайну",
#                     "name": "user"
#                 }
#             ]

# chat_response = client.create_chat_completion(
#     messages=messages,
#     temperature=0.9
# )
# print(chat_response)