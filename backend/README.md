# Backend
This part of the project implements server logic using **FastAPI**.
The backend accepts requests from clients, processes data, interacts with the database, and provides an API for working with vacancies and resumes.

### Setup
Запустите backend сервер:
```bash
poetry run gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)