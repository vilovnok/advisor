from typing import Dict, Literal

from agent.nodes._base import _BaseRouter
from agent.graphs.state import State


class ClassifierRouter(_BaseRouter):
    """
    Router Node to retranslate classifier node output to Retriever or Operator nodes.
    """

    def __init__(
        self,
        name: str,
        description: str,
        mapping: Dict,
        show_logs: bool = False,
    ) -> None:
        """
        Initialize the ClassifierRouter.

        Args:
            name (str): Name of the node.
            description (str): Description of the node's purpose.
            mapping (Dict): Mapping for routing decisions.
            show_logs (bool): Flag to enable or disable logging.
        """
        super().__init__(name, description, mapping)
        self.show_logs = show_logs

    def invoke(self, state: State) -> Literal["extract", "no_info"]:
        """
        Determine the next step based on the catalog and category names.

        Args:
            state (State): Current state of the workflow.

        Returns:
            Literal["extract", "no_info"]: Determines whether to return "profile" or "no_info".
        """
        
        similary_name = state.similary_name
        activity_name = state.activity_name
        category_name = state.category_name

        if self.show_logs:
            print(self.name)
            print(f"Category name: {category_name}")
            print(f"Activity name: {activity_name}")
            print("----------------")

        if similary_name:            
            if category_name not in ("resume", "vacancy"):
                return "no_info"
            elif activity_name not in ("devops", "frontend", "backend"):
                return "no_info"
            else:
                return "extract"
        else:
            return "no_info"