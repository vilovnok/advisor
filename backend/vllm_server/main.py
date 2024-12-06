# from openai import OpenAI
import asyncio
import openai

api_key = "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"
api_base = "http://localhost:7986/v1"

# openai.api_base = api_base
# openai.api_key = api_key


# client = OpenAI(
#     api_key=api_key,
#     base_url=api_base
# )

# response = client.completions.create(model="Qwen/Qwen2.5-1.5B-Instruct",
#                                       prompt="Расскажи мне историю.", max_tokens=512)
# print("Completion result:", response.choices[0].text)

import sys
sys.stdout.reconfigure(encoding='utf-8')


model="Qwen/Qwen2.5-1.5B-Instruct",
def talk():
    while True:
        text = input('user: ')
        if text == "q":
            break

        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-1.5B-Instruct",
            messages=[
                {"role": "system", "content": "Ты бот который всегда рассказывает правду."},
                {"role": "user", "content": f'{text}'},
            ],
            temperature=0.2,
            max_tokens=4096,
            top_p=0.6
        )
        print("bot:", response.choices[0].message.content)



def standart_gen():
    num_stories = 10
    prompt = "Я пошел в магазин и купил"

    for _ in range(num_stories):
        response = client.completions.create(
            model="Qwen/Qwen2.5-1.5B-Instruct",
            prompt=prompt,
            max_tokens=512,
        )

        print(prompt + response.choices[0].text)


def stat_gen():

    num_stories = 10
    prompts = ["Я пошел в магазин и купил"] * num_stories

    response = client.completions.create(
        model="Qwen/Qwen2.5-1.5B-Instruct",
        prompt=prompts,
        max_tokens=100,
    )
    
    stories = [""] * len(prompts)
    for choice in response.choices:
        stories[choice.index] = prompts[choice.index] + choice.text

    for story in stories:
        print(story)

# stat_gen()

def compile():
    

    
    from openai import AsyncOpenAI


    async_client = openai.AsyncOpenAI(api_key=api_key, base_url=api_base)

    data = [
        {"prompt": {"text": "Расскажи интересный факт о космосе."}},
        {"prompt": {"text": "Объясни, что такое искусственный интеллект."}},
        {"prompt": {"text": "Какая погода в Москве зимой?"}}
    ]

    async def generate_answers(prompt):
        completion = await async_client.chat.completions.create(
            model="mistralai/Mistral-Nemo-Instruct-2407",
            messages=[{"role": "user", "content": prompt}],
            # max_length=1028
        )
        print(completion.choices[0].message)
        return completion.choices[0].message.content

    # results = []
    batch_size = 128
    async def main(batch):
        tasks = []
        
        for idx, prompt in enumerate(batch):
            task = asyncio.create_task(generate_answers(prompt["prompt"]["text"]))
            tasks.append(task)

        answers = await asyncio.gather(*tasks)
        # results += answers


    for idx in range(0, len(data), batch_size):
        print()
        print
        asyncio.run(main(data[idx:idx+batch_size]))

compile()

def pop():

    import openai
    import asyncio

    client = openai.AsyncOpenAI(api_key=api_key, base_url=api_base)
    data = [
        {"prompt": {"text": "Расскажи интересный факт о космосе."}},
        {"prompt": {"text": "Объясни, что такое искусственный интеллект."}},
        {"prompt": {"text": "Какая погода в Москве зимой?"}}
    ]    

    async def generate_answers(prompt):
        completion = await client.chat.completions.create(
            model="Qwen/Qwen2.5-1.5B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            # max_tokens=1024,
            # request_timeout=10000
        )
        print(completion.choices[0].message)


    async def main(data):
        tasks = []
        for idx, prompt in enumerate(data):
            task = asyncio.create_task(generate_answers(prompt))
            tasks.append(task)

        answers = await asyncio.gather(*tasks)
        return answers

    # data- это набор данных, на котором генерируются ответы
    results = asyncio.run(main(data))
# pop()

# def setup_openai():
    # openai.api_key = "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"
    # openai.api_base = "http://localhost:7986"

# setup_openai()

# system_prompt = "Ты бот который отвечает очень грубо"
# user_prompt = "Как дела?"

# messages = [
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": user_prompt}
#     ]

# result = openai.ChatCompletion.create(
#             model="lmsys/vicuna-7b-v1.3",
#             messages=messages,
#             max_tokens=4096,
#             temperature=0.9,
#             top_p=0.6
#         )
# print(result["choices"][0].get("message").get("content"))




# # from .vllm_client import VLLMClient


# # client = VLLMClient(base_url="http://localhost:7986")
# # info_model = client.list_models()
# # model = info_model['data'][0]['id']

# # client = VLLMClient(base_url="http://localhost:7986", model=model)

# # Генерация эмбеддингов
# # embeddings = client.generate_embeddings(
# #     model="meta-llama/Llama-2-7b-hf",
# #     input_texts=["Пример текста для эмбеддингов."],
# #     encoding_format="float",
# #     dimensions=512,
# #     user="r1char9",
# #     truncate_prompt_tokens=1,
# #     additional_data=None,
# #     add_special_tokens=True,
# #     priority=1
# # )
# # print(embeddings)




# # completion = client.create_completion(
# #     prompt=["Расскажи историю"],
# #     max_tokens=1024,
# #     temperature=0.2
# # )
# # print(completion['choices'][0]['text'])


# # messages=[
# #                 {
# #                     "role": "system", 
# #                     "content": "You are a helpful assistant.",
# #                     "name": "bot"
# #                 },
# #                 {
# #                     "role": "user", 
# #                     "content": "Расскажи мне тайну",
# #                     "name": "user"
# #                 }
# #             ]

# # chat_response = client.create_chat_completion(
# #     messages=messages,
# #     temperature=0.9
# # )
# # print(chat_response)