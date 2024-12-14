from agent.benchmark.benchmark import Benchmark 
import pandas as pd


query_text = """
Вакансия: Frontend разработчик (TypeScript/React)
Опыт работы: От 3 до 6 лет
Описание: Разработка нового функционала и поддержка существующего в личных кабинетах и порталах банка, интеграция с внешними системами. Опыт работы на методологии Agile. 
Ключевые навыки: JavaScript, Git, Webpack, Node.js, TypeScript.
Тип занятости: полная занятость
График работы: удаленная работа
Знание языков:  Русский — Родной, Английский — B1 — Средний. 
Образование:  Высшее образование, техническое.
"""


models = [
    ["all-MiniLM-L6-v2", "bm25", "deepvk/USER-bge-m3", "colbertv2.0"],
    ["all-MiniLM-L6-v2", "bm25", "deepvk/USER-bge-m3"],
    ["deepvk/USER-bge-m3", "bm25", "colbertv2.0"],
    ["bm25", "deepvk/USER-bge-m3", "colbertv2.0"],
    ["all-MiniLM-L6-v2", "bm25", "colbertv2.0"],
    ["all-MiniLM-L6-v2", "bm25"],
    ["deepvk/USER-bge-m3", "bm25"],
    ["deepvk/USER-bge-m3"],
    ["all-MiniLM-L6-v2"],
    ["colbertv2.0"]
]


catalog = 'cv'
category = 'frontend'
limit = 10
ground_truth = "cv-frontend"

client = Benchmark(collection_name='advisor_db', url="http://localhost:6333")

metrics_table = client.benchmark(
    models=models, 
    ground_truth=ground_truth, 
    query_text=query_text,
    limit=10,
    # filter_options={'catalog':catalog}
)

print(metrics_table)
client.client.close()

# metrics_table.to_csv("metrics_table.csv", index=False)
