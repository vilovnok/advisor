import subprocess
from huggingface_hub import login

token = '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'
login(token=token)

command = [
    "python", "-m", "vllm.entrypoints.openai.api_server", 
    "--model", "msu-rcc-lair/RuadaptQwen2.5-32B-instruct-GGUF_Q3_K_M", 
    "--gpu-memory-utilization", "0.85",
    "--port", "7986"
]
subprocess.run(command)