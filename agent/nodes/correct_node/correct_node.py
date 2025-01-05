from langchain_core.output_parsers import StrOutputParser, BaseOutputParser
from langchain_core.messages import AIMessage

from .prompt import CORRECT_NODE_PROMPT
from agent.nodes._base import _BaseNode
from agent.llms._base import _BaseLLM
from agent.graphs.state import State


class CorrectNode(_BaseNode):
    """
    Correct answer of the model from the profile node.
    """

    def __init__(
        self,
        name: str,
        description: str,
        llm: _BaseLLM,
        prompt: str = CORRECT_NODE_PROMPT,
        output_parser: BaseOutputParser = StrOutputParser(),
        show_logs: bool = False,
    ) -> None:
        super().__init__(name, description, llm, prompt, output_parser)
        self.show_logs = show_logs

    def invoke(self, state: State) -> dict:
        """
        Executes the classifier node to process and classify the input query.

        Args:
            state (State): The current state object containing user context.

        Returns:
            dict: Updated state information.
        """
        history = state.history
        content = history[-1].content

        profile = self.vllm.invoke(content=content)
        clean_profile = profile.replace("```", "").strip()
        
        state.history.append(AIMessage(content=clean_profile))

        if self.show_logs:
            print(self.name)
            print(f"Model answer:\n\n{profile}")
            print("----------------")

        return {
            "history": history,
            "catalog_name": state.catalog_name,
            "category_name": state.category_name,
        }
