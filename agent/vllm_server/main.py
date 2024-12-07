import time
from .openai_client import OpenAIClient

client = OpenAIClient()


if __name__ == "__main__":
    while True:
        client.health_check()
        time.sleep(30)  