from langchain_mistralai import ChatMistralAI
from langchain.chains.combine_documents.stuff import StuffDocumentsChain

from agent.utils import get_system_prompt


class AdvisorLLM:
    def __init__(self, api_key, model) -> None:
        self.api_key = api_key
        self.model = model
        self.ttt=get_system_prompt()
        self._init_chain()
        self._init_prompts()

    def _init_chain(self):
        self.chat = ChatMistralAI(
            model=self.model,
            temperature=0.5,
            max_retries=2,
            api_key=self.api_key 
        )       

    def _init_prompts(self):
        self.system_prompt = get_system_prompt() 
 
    def invoke(self, query: str):
        messages = [
        ("system", self.system_prompt),
        ("human", query),
        ]
        response = self.chat.invoke(messages)
        return response