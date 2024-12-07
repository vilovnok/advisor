from agent.graphs import ConsultantGraph
from agent.utils import LlmModelType


with open('agent/example.txt', 'r', encoding='utf-8') as file:
    content = file.read()
# content='Привет, как дела?'
if __name__ == "__main__":

    name = 'Mistral'
    model_name = "mistral-large-latest"
    model_type = LlmModelType.MISTRAL

    graph = ConsultantGraph(
                            # name=name,
                            # model_name=model_name,
                            # model_type=model_type,
                            show_logs=True, 
                            save_online_metric=False)
    graph.chat(content)

