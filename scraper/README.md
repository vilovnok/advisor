# Parser
## Run to get the data
```bash
poetry run python scraper/main.py --topic "Devops разработчик" --area 1  --limit_page 4 --limit_objects 100
```
## Create a new dataset
```bash
poetry run python scraper/forge_dataset.py
```

## Create and fill a new database
```bash
poetry run python agent/database/main.py --act delete --coll_name it_area
```


1) создать метод который автономно создает файл dataset на уровне backend

2) для хостинга моделей на локальном уровне vllm или sqlang

3) Нужно для CV испраить парсинг "location" и "description"