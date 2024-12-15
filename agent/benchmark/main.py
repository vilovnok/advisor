from agent.benchmark.benchmark import Benchmark 
import pandas as pd


query_text = """
Резюме: Backend разработчик Опыт работы: 4 года 1 месяц Описание: Занимался backend разработкой и созданием сайтов. Ключевые навыки: Работоспособность, • Коммуникабельность, способность устанавливать контакты, • Инициативность, • Ответственность, • Отзывчивость Тип занятости: полная занятость, частичная занятость График работы: полный день, гибкий график Знание языков: Кыргызский — Родной, Английский — B2 — Средне-продвинутый, Русский — C2 — В совершенстве Образование: Неоконченное высшее образование, техническое
"""


models = [
    ["all-MiniLM-L6-v2", "bm25", "deepvk/USER-bge-m3", "colbertv2.0"],
    ["all-MiniLM-L6-v2", "bm25", "deepvk/USER-bge-m3"],
    ["deepvk/USER-bge-m3", "bm25", "colbertv2.0"],
    ["bm25", "deepvk/USER-bge-m3", "colbertv2.0"],
    ["all-MiniLM-L6-v2", "bm25", "colbertv2.0"],
    ["all-MiniLM-L6-v2", "bm25"],
    ["deepvk/USER-bge-m3", "bm25"],
    ["deepvk/USER-bge-m3","colbertv2.0"],
    ["deepvk/USER-bge-m3","all-MiniLM-L6-v2"],
    ["all-MiniLM-L6-v2", "colbertv2.0"],
    ["deepvk/USER-bge-m3"],
    ["all-MiniLM-L6-v2"],
    ["colbertv2.0"]
]


catalog = 'vac'
category = 'backend'
ground_truth = f"{catalog}-{category}"

client = Benchmark(collection_name='advisor_db', url="http://localhost:6333")

metrics_table = client.benchmark(
    models=models, 
    ground_truth=ground_truth, 
    query_text=query_text,
    topK=10,
    limit=15,
    filter_options={'catalog':catalog}
)

print(metrics_table)
client.client.close()

# metrics_table.to_csv("metrics_table.csv", index=False)
