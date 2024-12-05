import openai
import paramiko
import subprocess
import time

# Создаем SSH-туннель
def create_ssh_tunnel():
    ssh_host = "77.234.216.100"
    ssh_user = "rgurtsiev"
    ssh_password = "ohshieN1aiG9"
    remote_host = "10.196.183.10"
    remote_port = 7986
    local_port = 8881

    # Создаем SSH клиент
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Подключаемся к удаленному серверу
    ssh_client.connect(ssh_host, username=ssh_user, password=ssh_password)
    
    # Создаем SSH-туннель
    ssh_client.get_transport().request_port_forward('localhost', local_port, remote_host, remote_port)
    
    print(f"SSH Tunnel established on localhost:{local_port} to {remote_host}:{remote_port}")

    return ssh_client

# Настроим OpenAI API
def setup_openai():
    openai.api_base = "http://localhost:7986"

# Запустим код
def main():
    # Создаем SSH туннель
    ssh_client = create_ssh_tunnel()

    # Настроим OpenAI API
    setup_openai()

    # Пример запроса к OpenAI API
    system_prompt = "Your system prompt"
    
    # Отправляем запрос
    response = openai.Completion.create(
        model="meta-llama/Llama-2-7b-hf",
        prompt=system_prompt,
        max_tokens=50
    )

    print("Response:", response)

    # Ожидаем, пока SSH-туннель не будет закрыт вручную
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Closing SSH tunnel.")
        ssh_client.close()

if name == "__main__":
    main()