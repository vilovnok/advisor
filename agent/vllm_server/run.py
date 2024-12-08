import subprocess
from .utils import hf_key
from huggingface_hub import login
from agent.utils import LlmModelType


login(token=hf_key)

command = [
    "python", "-m", "vllm.entrypoints.openai.api_server", 
    "--model", f"{LlmModelType.QWEN}",
    "--gpu-memory-utilization", "0.85",
    "--port", "7986"
]
subprocess.run(command)