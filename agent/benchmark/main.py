from agent.benchmark.benchmark import Benchmark 


models = [

    # Single model
    # ["bm25"],
    # ["all-MiniLM-L6-v2"],
    # ["deepvk/USER-bge-m3"],
    # ['intfloat/multilingual-e5-large'],
    # ["Tochka-AI/ruRoPEBert-e5-base-2k"],
    # ["cointegrated/rubert-tiny2"],
    
    # Reciprocal Rank Fusion method
    # ["deepvk/USER-bge-m3", "bm25"],
    # ['intfloat/multilingual-e5-large', "bm25"],
    # ["Tochka-AI/ruRoPEBert-e5-base-2k", "bm25"],
    # ["cointegrated/rubert-tiny2", "bm25"],
    # ["all-MiniLM-L6-v2", "bm25"],
    ## ["colbertv2.0", "bm25"],

    # # Matryoshka
    # ["ruRoPEBert->multilingual->deepvk+bm25"],
    # ["Tochka-AI/ruRoPEBert-e5-base-2k+bm25"],
    # ['intfloat/multilingual-e5-large+bm25'],
    # ["cointegrated/rubert-tiny2+bm25"],
    # ["bm25->ruRoPEBert-e5-base-2k->USER-bge-m3"]
    
]

query_text = """
Резюме: Backend разработчик Опыт работы: 4 года 1 месяц Описание: Занимался backend разработкой и созданием сайтов. Ключевые навыки: Работоспособность, • Коммуникабельность, способность устанавливать контакты, • Инициативность, • Ответственность, • Отзывчивость Тип занятости: полная занятость, частичная занятость График работы: полный день, гибкий график Знание языков: Кыргызский — Родной, Английский — B2 — Средне-продвинутый, Русский — C2 — В совершенстве Образование: Неоконченное высшее образование, техническое
"""


catalog = 'vac'
category = 'backend'
ground_truth = f"{catalog}-{category}"

client = Benchmark(collection_name='advisor_last_db', url="http://localhost:6333")

metrics_table = client.benchmark(
    models=models, 
    ground_truth=ground_truth, 
    query_text=query_text,
    topK=10,
    limit=20,
    filter_options={'catalog':catalog}
)

print(metrics_table)
client.client.close()

metrics_table.to_csv("metrics_table.csv", index=False)
