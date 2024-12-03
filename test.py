from vllm import LLM, SamplingParams
from huggingface_hub import login

MODEL_PATH = "mistralai/Mistral-7B-Instruct-v0.3"

token='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'
login(token=token)
# Инициализируйте LLM
llm = LLM(model=MODEL_PATH)

# 2. Определение параметров сэмплирования
sampling_params = SamplingParams(
    temperature=0.7,
    max_tokens=200,
    top_p=0.9,
    top_k=40
)

# 3. Функция для инференса
def generate_response(prompt: str) -> str:
    """Генерирует текст на основе заданного prompt."""
    results = llm.generate(prompt, sampling_params)
    # Возвращаем только текстовый результат
    return results[0].outputs[0].text

# 4. Пример использования
if __name__ == "__main__":
    # Задайте prompt
    user_prompt = "Напиши историю про путешественника, который исследует загадочный лес."
    response = generate_response(user_prompt)
    
    print(f"Prompt: {user_prompt}")
    print(f"Response: {response}")
