from langchain_core.output_parsers import StrOutputParser, BaseOutputParser

from .prompt import CLASSIFIER_NODE_PROMPT
from agent.nodes._base import _BaseNode
from agent.llms._base import _BaseLLM
from agent.graphs.state import State


class ClassifierNode(_BaseNode):
    """
    Classifier Node to classify input query (user input) in categories.
    """

    def __init__(
        self,
        name: str,
        description: str,
        llm: _BaseLLM,
        prompt: str = CLASSIFIER_NODE_PROMPT,
        output_parser: BaseOutputParser = StrOutputParser(),
        show_logs: bool = False,
    ) -> None:
        """
        Initialize the ClassifierNode.

        Args:
            name (str): Name of the node.
            description (str): Description of the node's purpose.
            llm (_BaseLLM): LLM for generating responses.
            prompt (str): Prompt for the LLM.
            output_parser (BaseOutputParser): Parser to process the output.
            show_logs (bool): Flag to enable or disable logging.
        """
        super().__init__(name, description, llm, prompt, output_parser)
        self.show_logs = show_logs

    def invoke(self, state: State):
        """
        Classify input query into categories.

        Args:
            state (State): Current state of the workflow.

        Returns:
            dict: A dictionary containing updated history and category info.
        """
        history = state.history
        content = history[-1].content

        catalog_name = 'vac' if "cv" in content else 'vac'
        category_name = self.vllm.invoke(content=content)

        if self.show_logs:
            print(self.name)
            print(f"Model answer: \ncatalog: {catalog_name}\ncategory: {category_name}")
            print("----------------")

        return {
            "history": history,
            "catalog_name": catalog_name,
            "category_name": category_name,
        }
