import re
from typing import List
from langchain_core.output_parsers import StrOutputParser, BaseOutputParser
from langchain_core.messages import BaseMessage, AIMessage

from .prompt import ANSWER_NODE_PROMPT
from agent.nodes._base import _BaseNode
from agent.llms._base import _BaseLLM
from agent.graphs.state import State

from agent.nodes.answer_node.methods.calculate_skills import (calculate_similarity_score)

class AnswerNode(_BaseNode):
    """
    Answer Node to generate answer based on data catalog.
    """
    def __init__(
            self,
            name: str,
            description: str,
            llm: _BaseLLM,
            prompt: str = ANSWER_NODE_PROMPT,
            output_parser: BaseOutputParser = StrOutputParser(),
            show_logs: bool = False,
        ) -> None:
        super().__init__(name, description, llm, prompt, output_parser)
        self.show_logs = show_logs


    def rank_examples(self, history: List[BaseMessage]):
        examples = history[-1].content
        target = history[-2].content

        blocks = re.split(r'\n\s*\n', examples.strip())
        examples =  [block.strip() for block in blocks if block.strip()]

        result = calculate_similarity_score(target, examples)
        
        # return "\n\nTarget:\n" + target.split('Ключевые навыки')[0] + "\n\n".join([res for res in result])
        sorted_objs = sorted(result, key=result.get, reverse=True)
        return sorted_objs

    def invoke(self, state: State):
        history = state.history
        answer = self.rank_examples(history)

        # answer = self.vllm.invoke(content=content)

        if self.show_logs:
            print(self.name)
            print(f"User query: summary")
            print(f"GET Data:")

            print(f'Answer: {answer}')

            print("----------------")

        return {"history": history, "catalog_name": state.catalog_name, "hallucination": state.hallucination, "category_name": state.category_name}
