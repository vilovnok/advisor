import uvicorn
from vllm import LLM, SamplingParams
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api_model.schema import (ChatRequest, ChatResponse, ChatResponseChoice)

from huggingface_hub import login

model = "meta-llama/Llama-2-7b-hf"
token='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'

login(token=token)

app = FastAPI(title='vLLM')
llm = LLM(model=model)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin","Authorization"],
)

@app.post("/v1/chat/completions", response_model=ChatResponse)
async def chat_completions(request: ChatRequest):
    if request.model != model: 
        raise HTTPException(status_code=400, detail="Model not found")

    prompt = ""
    for message in request.messages:
        role = message.role.capitalize()
        prompt += f"{role}: {message.content}\n"
    prompt += "Assistant:"

    sampling_params = SamplingParams(
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
    )

    outputs = llm.generate(prompt, sampling_params)


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

@app.get("/v1/models")
async def list_models():
    return {
        "data": [{"id": model, "object": "model"}],
        "object": "list",
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7896)