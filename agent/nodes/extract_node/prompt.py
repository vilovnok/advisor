EXTRACT_EDUCATION_PROMPT = """
You will be provided with customer service queries, delimited by '###'.
Extract only the candidate's education details: degree, specialization, educational institution, and study period.

Important:
- Do not repeat any details.
- Do not include questions, comments, or explanations.
- Provide a concise and unique response strictly containing education-related information.

Query:
{context}

Answer:
"""
CLS_EDUCATION_PROMPT = """
You will be provided with customer service queries. The query will be delimited with '###'. 
Classify the candidate's education based on the following:

    Categories:
    - Technical education
    - Non-technical education
    - Education not specified

Analyze the following examples to correctly determine the education category:  

Example 1:  
    Query: Graduated from Saint Petersburg Polytechnic University, majoring in Software Engineering, bachelor's degree.  
    Question: Which university did the candidate graduate from?  
    Answer: Polytechnic University, majoring in Software Engineering.  
    Question: Is this major technical?  
    Answer: Yes, software engineering is technical.  
    Final Answer: Technical education.

Example 2:
    Query: Earned a degree in economics from the Financial University under the Government of the Russian Federation.  
    Question: Which university did the candidate graduate from?  
    Answer: Financial University under the Government of the Russian Federation.  
    Question: Is this major technical?  
    Answer: No, finance is not technical.  
    Final Answer: Non-technical.

Example 3:
    Query: Graduated from Bauman Moscow State Technical University, majoring in Mechatronics and Robotics.  
    Question: Which university did the candidate graduate from?  
    Answer: Bauman Moscow State Technical University.  
    Question: Is this major technical?  
    Answer: Yes, robotics is technical.  
    Final Answer: Technical education.

Example 4:
    Query: Earned a bachelor's degree in International Relations from Moscow State University.  
    Question: Which university did the candidate graduate from?  
    Answer: Moscow State University.  
    Question: Is this major technical?  
    Answer: No, international relations is not technical.  
    Final Answer: Non-technical. 

Example 5:
    Query: I worked at McDonald's, was a cleaner, and taught Russian to children.  
    Question: Which university did the candidate graduate from?  
    Answer: Not specified.  
    Question: Is this major technical?  
    Answer: Not specified.  
    Final Answer: Education not specified.

Important:
    - Respond only with one of the following categories: "Technical education", "Non-technical education", or "Education not specified."
    - If the query mentions a technical field (e.g., software engineering, robotics, mechatronics), classify as "Technical education."
    - If the query mentions a non-technical field (e.g., economics, international relations, history), classify as "Non-technical education."
    - If no education is mentioned, classify as "Education not specified."
    - Do not include questions, comments, or explanations.
    - Do not answer any questions, your answer should concern only one of the previously listed classes.

Candidate's education:
    {context}

Final Answer: 
"""
CORRECT_EDUCATION_PROMPT = """
You will be provided with customer service queries, delimited by '###'.
Extract only the eduaction in json format {edu: eduaction}, where education: Technical education, Non-technical education, Education not specified.
----------

Important:
    - Do not include questions, comments, or explanations.
---------

Education information:
{context}

Answer: json format
"""



EXTRACT_LANGUADE_PROMPT = """
You will be provided with customer service queries, delimited by '###'.
Extract only the language(s) spoken by the candidate communication.

Important:
    - Do not repeat any details.
    - Do not include questions, comments, or explanations.
    - If no information about languages is provided, return "Русский — родной."
    - Provide a concis, unique, and clear response with only languages mentioned.

Query:
{context}

Answer: only language(s)
"""
CORRECT_LANGUAGE_PROMPT = """
You will be provided with customer service queries, delimited by '###'.
Extract only the language(s) in json format in json format {language: []}.

----------
Important:
    - Do not include questions, comments, or explanations.
---------

Language information:
{context}

Answer:
"""


EXTRACT_EMPLOYMENT_PROMPT = """
You will be provided with customer service queries, delimited by '###'.
Extract only the candidate's employment type in json format {emp: [employment]}, where employment: полная занятость, частичная занятость, проектная работа, стажировка.

Important:
    - Do not repeat any details.
    - Do not include questions, comments, or explanations.
    - If the employment type is mentioned multiple times, return it only once.
    - Return only the unique employment type(s) mentioned.
    - Provide a clear, concise response with only the employment types mentioned, without any extra information.
    - If no information about employment is provided, return "полная занятость".

Candidate's employment:
{context}

Answer:
"""
CORRECT_EMPLOYMEN_PROMPT = """
You will be provided with customer service queries, delimited by '###'.
Extract only the employment in json format {employ: [employment]}.

----------
Important:
    - DO NOT INCLUDE QUESTION, COMMENT AND EXPLONATION. 
    - Do NOT REPEAT ANSWER.
---------

Employment information:
{context} 

Answer: json format
"""


EXTRACT_SCHEDULE_PROMPT = """
You will be provided with customer service queries, delimited by '###'.
Extract only the candidate's schedule type: полный день, гибкий график, удаленная работа.
Each schedule type should appear only once.

Important:
    - Do not repeat any details.
    - Do not include questions, comments, or explanations.
    - If the schedule type is mentioned multiple times, return it only once.
    - Return only the unique schedule type(s) mentioned.
    - Provide a clear, concise response with only the schedule types mentioned, without any extra information.
    - If no information about schedule is provided, return "полный день".

Candidate's schedule:
{context}

Answer: only schedule type
"""
CORRECT_SCHEDULE_PROMPT = """
You will be provided with customer service queries, delimited by '###'.
Extract only the schedule in json format {she: [schedule]}, where schedule: полный день, гибкий график, удаленная работа.

----------
Important:
    - Do not include questions, comments, or explanations.
---------

Schedule information:
{context}

Answer: json format
"""


EXTRACT_SKILLS_PROMPT = """
You will be provided with customer service queries, delimited by '###'.
Extract only the candidate's skills: technical skills, soft skills.

Important:
    - Do not repeat any details.
    - Do not include questions, comments, or explanations.
    - Provide a concise and unique response strictly containing the candidate’s skills.

Query:
{context}

Answer: 
"""
CORRECT_SKILLS_PROMPT = """
You will be provided with customer service queries, delimited by '###'.
Extract only the candidate's skills in json format {technical_skills: [], soft_skills: []}.
Answer must be json format {technical_skills: [], soft_skills: []}.

----------
Important:
    - Do not repeat answer.
    - Do not include questions, comments, or explanations.
---------

Candidate's skills:
{context}

Answer: json format
"""


EXTRACT_EXPERIENCE_PROMPT = """
You will be provided with customer service queries, delimited by '###'.
Extract only the candidate's work experience durations in the format: "X years Y months."

Important:
    - List only information related to work experience.
    - Do not repeat information.
    - Do not include questions, comments, or explanations.
    - Determine the user's total work experience from the provided resume in the format: [X years Y months]. If exact data is not available, make a reasonable assumption.

Query:
{context}

Answer: only information about the candidate's work experience
"""
CORRECT_EXPERIENCE_PROMPT = """
You will be provided with customer service queries, delimited by '###'.
Extract only the work experience in json format {work_experience: "X years Y months"}.

----------
Important:
    - The total should be returned as a single value in the format "X years Y months."
    - Do not include questions, comments, or explanations.
---------

Work experience information:
{context}

Answer: json format
"""

EXTRACT_DESCRIPTION_PROMPT = """ 
You will be provided with customer service queries, delimited by '###'.
Extract only the information about the candidate, what they did in their positions.

Specify their responsibilities and key tasks.
Ignore information about their name, company, dates of employment, and anything unrelated to their duties and tasks.
Only output the description of responsibilities and tasks, avoiding unnecessary details.

The answer should be in a single line and in Russian.

Query:
{context}

Answer:
"""