from agent.utils import LlmModelType
from .utils import openai_key, api_base
from .openai_client import OpenAIClient



client = OpenAIClient(model_type=LlmModelType.QWEN, api_base=api_base, api_key=openai_key)
response = client.invoke(
            """
            Суммаризуй текст, выдели из текста информацию про обязаности пользователя,
            ключевые задачи.             
            Ответ должен быть в строчку. 
            """,
            """
            Компания занимается разработкой и внедрением инновационных решений для пассажирского транспорта, используя Java 8, 17, Spring framework, Spring Boot, JPA, Cloud, Security, AOP, Test Containers, Junit 4,5, Mockito, Kafka, PostgreSQL 14.5, PromQL, Grafana, Linux, Docker, Git, Tomcat, Netty, SSL, TLS, HTTP, HTTPS, Maven, Gradle, Gitlab CI/CD; требует уверенных знаний Java Core 8, 17, опыта работы с Spring Framework, Spring Boot, Spring JPA, Hibernate, JUnit, Mockito, Test Containers, SQL, инструментами разработки Gradle, Maven, Docker, Git, баг-трекерами (Taiga, Mantis и подобные), знание платежных систем и интеграции с платежными шлюзами, технологий смарт-карт, интеграции ККТ, ясный ум и умение разбираться и обучаться; кандидат будет заниматься бэк-энд разработкой для высоконагруженных сервисов, в том числе мобильных (автоматизация бизнеса, отрасли, платежи, приложения); компания предлагает аккредитованную IT-компанию, ДМС, внешнее обучение за счет компании, годовой бонус по результатам Performance Review, формат работы - офис, с возможностью перехода на гибридный график (г. Москва).
            """)