# Advisor
[View Presentation](https://docs.google.com/presentation/d/1MfScovZ28nzBBk5KeICxhf5TCSnhVDVovYoiV2m7L3s/edit?usp=sharing)

![metrics](https://habrastorage.org/r/w1560/getpro/habr/upload_files/47c/fe1/30f/47cfe130fd789300b1bfaf2baf9e52aa.jpg)
---

**Advisor** is a system designed to provide personalized recommendations for both candidates and HR agents. The primary goal of the project is to automate the matching of the most suitable vacancies or resumes based on input content analysis.

---

## 🛠  Core Features

- **Personalized Recommendations**
  - For candidates: Suggesting top vacancies that match their skills and experience.
  - For HR agents: Finding resumes that meet the vacancy requirements.

- **RAG System (Retrieval-Augmented Generation)**
  - Processes and analyzes input data (resumes or job vacancies).
  - Enhances recommendation quality by integrating information from multiple sources.

- **Content Analysis**
  - Intelligent text processing to extract key parameters such as skills, work experience, job requirements, and other factors indicating suitability.

---

## 📈 System Advantages

- Reduces the time needed to find relevant vacancies or resumes.
- High recommendation accuracy powered by modern data analysis algorithms.
- User-friendly for both job seekers and HR specialists.

---

Advisor streamlines the employment process and makes interactions between candidates and employers more efficient.


## ⚙️ Setup Instructions

1. Start Docker containers:
```bash
docker-compose up -d
```

2. Install dependencies:
```bash
poetry install
```

3. Activate the virtual environment:
```bash
poetry shell
```

4. Start the vLLM server with the QWEN model:
```bash
poetry run python -m agent.vllm_server.run
```

5. Fetch data from HeadHunter  
For example, load 100 vacancies and resumes:
```bash
poetry run python scraper/main.py --topic "Devops разработчик" --area 1  --limit_page 4 --limit_objects 100
```

6. Convert the fetched data into CSV files:
```bash
poetry run python scraper/forge_dataset.py
```

7. Create a collection in Qdrant
```bash
poetry run python agent/database/main.py --act create --coll_name advisor_db
```

8. Upload the processed data to Qdrant
```bash
poetry run python agent/database/main.py --act upload --coll_name advisor_db
```

9. Start the backend API for interaction with the agent
```bash
poetry run python -m backend.main
```

10. Open the web interface at [http://localhost:4200](http://localhost:4200)