from agent.graphs import ConsultantGraph




with open('agent/example.txt', 'r', encoding='utf-8') as file:
    content = file.read()

if __name__ == "__main__":
    graph = ConsultantGraph(show_logs=True, save_online_metric=False)
    graph.chat(content)

