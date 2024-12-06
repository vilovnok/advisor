import subprocess
from huggingface_hub import login

token = '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'
login(token=token)

command = [
    "python", "-m", "vllm.entrypoints.openai.api_server", 
    "--model", "meta-llama/Llama-3.2-3B-Instruct",
    "--gpu-memory-utilization", "0.85",
    "--port", "7986"
]
subprocess.run(command)