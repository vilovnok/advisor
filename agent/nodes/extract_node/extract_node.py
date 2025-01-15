from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser, BaseOutputParser
from agent.nodes._base import _BaseNode
from agent.llms._base import _BaseLLM
from agent.graphs.state import State

from .prompt import (
    CLS_EDUCATION_PROMPT, EXTRACT_EDUCATION_PROMPT, EXTRACT_LANGUADE_PROMPT, 
    EXTRACT_EMPLOYMENT_PROMPT, EXTRACT_SCHEDULE_PROMPT, CORRECT_SCHEDULE_PROMPT,
    CORRECT_EDUCATION_PROMPT, CORRECT_LANGUAGE_PROMPT, EXTRACT_SKILLS_PROMPT, 
    EXTRACT_EXPERIENCE_PROMPT, CORRECT_EXPERIENCE_PROMPT, CORRECT_SKILLS_PROMPT,
    EXTRACT_DESCRIPTION_PROMPT
)

from agent.utils import conv_to_json, generate_summary


class ExtractNode(_BaseNode):
    """
    Profile Node to create a user profile.
    """

    def __init__(
        self,
        name: str,
        description: str,
        llm: _BaseLLM,
        prompt: str = EXTRACT_LANGUADE_PROMPT,
        output_parser: BaseOutputParser = StrOutputParser(),
        show_logs: bool = False,
    ) -> None:
        super().__init__(name, description, llm, prompt, output_parser)
        self.show_logs = show_logs


    def invoke(self, state: State) -> dict:
        history = state.history
        content = history[-1].content
        
        education = self.vllm.Completion(content=content, prompt=EXTRACT_EDUCATION_PROMPT)
        education = self.vllm.Completion(content=education, prompt=CLS_EDUCATION_PROMPT)
        education = self.vllm.Completion(content=education, prompt=CORRECT_EDUCATION_PROMPT)
        education = conv_to_json(education)
        education = education['edu']

        language = self.vllm.Completion(content=content, prompt=EXTRACT_LANGUADE_PROMPT)
        language = self.vllm.Completion(content=language, prompt=CORRECT_LANGUAGE_PROMPT)
        language = conv_to_json(language)
        language = language['language']
        language = ", ".join(language)

        employment = self.vllm.Completion(content=content, prompt=EXTRACT_EMPLOYMENT_PROMPT)
        employment = conv_to_json(employment)
        employment = employment['emp']
        employment = ", ".join(employment)

        schedule = self.vllm.Completion(content=content, prompt=EXTRACT_SCHEDULE_PROMPT)
        schedule = self.vllm.Completion(content=schedule, prompt=CORRECT_SCHEDULE_PROMPT)
        schedule = conv_to_json(schedule)
        schedule = schedule['she']
        schedule = ", ".join(schedule)

        skills = self.vllm.Completion(content=content, prompt=EXTRACT_SKILLS_PROMPT)
        skills = self.vllm.Completion(content=content, prompt=CORRECT_SKILLS_PROMPT)
        skills = conv_to_json(skills)
        skills = skills['technical_skills'] + skills['soft_skills']
        skills = ", ".join(skills)

        experience = self.vllm.Completion(content=content, prompt=EXTRACT_EXPERIENCE_PROMPT)
        experience = self.vllm.Completion(content=experience, prompt=CORRECT_EXPERIENCE_PROMPT)
        experience = conv_to_json(experience)
        experience = experience['work_experience']

        description = self.vllm.Completion(content=content, prompt=EXTRACT_DESCRIPTION_PROMPT)

        data = {
            "experience": experience,
            "description": description,
            "skills": skills,
            "employment": employment,
            "schedule": schedule,
            "language": language,
            "education": education
        }
        profile = generate_summary(data=data)
        state.history.append(AIMessage(content=profile))
        
        if self.show_logs:
            print(self.name)
            print(f"Model answer:")
            print(f"\education: {education}\n")
            print(f"\language: {language}\n")
            print(f"\employment: {employment}\n")
            print(f"\schedule: {schedule}\n")
            print(f"\skills: {skills}\n")
            print(f"\experience: {experience}\n")
            print(f"\description: {description}\n")
            print("----------------")

        return {
            "history": history,
            "activity_name": state.activity_name,
            "category_name": state.category_name,
        }
