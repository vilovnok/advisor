import re
from typing import List

from langchain_core.messages import BaseMessage
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.output_parsers import StrOutputParser


from agent.database import Retriever
from agent.graphs.state import State
from agent.llms._base import _BaseLLM
from agent.nodes._base import _BaseNode
from agent.nodes.answer_node.methods.calculate_skills import SimilarityCalculator
from agent.nodes.answer_node.methods.extract_job_info import extract_job_info
from .prompt import ANSWER_NODE_PROMPT


class AnswerNode(_BaseNode):
    """
    Answer Node to generate an answer based on data catalog.
    """

    DATABASE_COLLECTION_NAME = "advisor_db"

    def __init__(
        self,
        name: str,
        description: str,
        llm: _BaseLLM,
        prompt: str = ANSWER_NODE_PROMPT,
        retriever: Retriever = None,
        output_parser: BaseOutputParser = StrOutputParser(),
        show_logs: bool = False,
    ) -> None:
        super().__init__(name, description, llm, prompt, output_parser)
        self.show_logs = show_logs
        self.retriever = Retriever(device=0) if not retriever else retriever

    def rank_examples(self, history: List[BaseMessage]) -> List[int]:
        """
        Rank examples from history based on similarity to the target.

        Args:
            history (List[BaseMessage]): The conversation history.

        Returns:
            List[int]: A list of ranked example IDs.
        """

        examples = history[-1].content
        target = history[-2].content

        blocks = re.split(r"\n\s*\n", examples.strip())
        examples = [block.strip() for block in blocks if block.strip()]
        calculator = SimilarityCalculator()
        results = calculator.calculate_similarity_score(target, examples)

        sorted_objs = sorted(results, key=results.get, reverse=True)
        return list(map(int, sorted_objs))


    def invoke(self, state: State) -> dict:
        """
        Invoke the node to process the state and return results.

        Args:
            state (State): The state object containing history and other data.

        Returns:
            dict: The processed results.
        """
        history = state.history
        point_ids = self.rank_examples(history=history)
        points = self.retriever.search_points(
            point_ids=point_ids, collection_name=AnswerNode.DATABASE_COLLECTION_NAME
        )

        points = [{"title":f"{extract_job_info(point.payload['content'])}","value": point.payload['content']} for point in points]

        history.append(AIMessage(
            name="AnswerNode",
            content=points
        ))

        if self.show_logs:
            print(self.name)
            print(f"Answer: {points}")
            print("----------------")

        return {
            "history": history,
            "catalog_name": state.catalog_name,
            "hallucination": state.hallucination,
            "category_name": state.category_name,
        }