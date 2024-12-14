import subprocess
from .utils import hf_key
from huggingface_hub import login


login(token=hf_key)

command = [
    "python", "-m", "vllm.entrypoints.openai.api_server", 
    "--model", "Qwen/Qwen2.5-7B-Instruct",
    "--gpu-memory-utilization", "0.85",
    "--port", "7986"
]
subprocess.run(command)