import openai
import time
from sshtunnel import SSHTunnelForwarder

def create_ssh_tunnel():
    ssh_host = "77.234.216.100"
    ssh_user = "rgurtsiev"
    ssh_password = "ohshieN1aiG9"
    remote_host = "10.196.183.10"
    remote_port = 1111
    local_port = 7986

    
    tunnel = SSHTunnelForwarder(
        (ssh_host, 22),
        ssh_username=ssh_user,
        ssh_password=ssh_password,
        remote_bind_address=(remote_host, remote_port),
        local_bind_address=('localhost', local_port)
    )
    
    # Запускаем туннель
    tunnel.start()
    print(f"SSH Tunnel established on localhost:{local_port} to {remote_host}:{remote_port}")
    return tunnel

def setup_openai():
    openai.api_key = "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"
    openai.api_base = "http://localhost:7986"
    

def main():
    # Создаем SSH туннель
    # tunnel = create_ssh_tunnel()

    # Настроим OpenAI API
    setup_openai()

    # Пример запроса к OpenAI API
    system_prompt = "Ты агент, который отвечает очень грубо!"
    user_prompt = "Как дела?"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    result = openai.Completion.create(
        model="meta-llama/Llama-2-7b-hf",
        prompt=messages,
        max_tokens=4096,
        temperature=0.9,
        top_p=0.6
    )

    print(result["choices"][0].get("text"))

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Closing SSH tunnel.")
        # tunnel.stop()

if __name__ == "__main__":
    main()