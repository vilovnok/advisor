from src import AdvisorLLM


api_key = 'vyhXlcO3zjBdbeHD0mmNMQf4PlBtIlM4'
llm = AdvisorLLM(api_key=api_key, model='model')

def test_prompt():
    output = llm.invoke('*')
    print('*'*50)
    print(output)
    assert output != ''
