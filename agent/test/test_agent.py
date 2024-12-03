from agent.src import AdvisorLLM
from agent.util import get_model_info


def selected_model(model_name: str):
    model_info = get_model_info(model_name)
    if model_info:
        model = model_info['model']
        api_key = model_info['api_key']
        return model, api_key
    else:
        raise ValueError(f"Модель '{model_name}' не найдена.")



def test_prompt():
    model_name = "Mistral"
    model, api_key = selected_model(model_name=model_name)
    llm = AdvisorLLM(api_key=api_key, model=model)
    output = llm.invoke('Как похудеть?')
    assert output.content != ''