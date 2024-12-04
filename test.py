from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from vllm import LLM, SamplingParams
from huggingface_hub import login



MODEL_PATH = "mistralai/Mistral-7B-Instruct-v0.3"
token='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'


login(token=token)




app = FastAPI()


llm = LLM(model="your_model_path")


class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    max_tokens: int = 256
    temperature: float = 0.7
    top_p: float = 0.9

class ChatResponseChoice(BaseModel):
    message: Dict[str, str]

class ChatResponse(BaseModel):
    choices: List[ChatResponseChoice]

# Эндпоинт для ChatCompletion
@app.post("/v1/chat/completions", response_model=ChatResponse)
async def chat_completions(request: ChatRequest):
    if request.model != "your_model_name":  # Проверяем имя модели
        raise HTTPException(status_code=400, detail="Model not found")

    # Объединение сообщений в один prompt
    prompt = ""
    for message in request.messages:
        role = message.role.capitalize()
        prompt += f"{role}: {message.content}\n"
    prompt += "Assistant:"

    # Настройки генерации текста
    sampling_params = SamplingParams(
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
    )

    # Генерация текста с моделью
    outputs = llm.generate(prompt, sampling_params)

    # Возвращаем первый результат
    content = outputs[0].outputs[0].text.strip()
    return ChatResponse(
        choices=[
            ChatResponseChoice(
                message={
                    "role": "assistant",
                    "content": content,
                }
            )
        ]
    )

# Эндпоинт для получения списка доступных моделей
@app.get("/v1/models")
async def list_models():
    return {
        "data": [{"id": "your_model_name", "object": "model"}],
        "object": "list",
    }