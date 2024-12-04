import subprocess

token = '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'

from huggingface_hub import login

login(token=token)

command = [
    "python", "-m", "vllm.entrypoints.openai.api_server", 
    "--model", "meta-llama/Llama-2-7b-hf", 
    "--gpu-memory-utilization", "0.85",
    "--port", "7986"
]

subprocess.run(command)