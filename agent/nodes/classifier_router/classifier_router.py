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
            show_logs: bool = False
        ):
        super().__init__(name, description, mapping)
        self.show_logs = show_logs

    def invoke(self, state: State) -> Literal["retriever", "no_info", "end"]:
        catalog_name = state.catalog_name
        category_name = state.category_name

        if self.show_logs:
            print(self.name)
            print(f"Catalog  name: {catalog_name}")
            print(f"Category name: {category_name}")
            print("----------------")

        if catalog_name and category_name:
            if catalog_name not in ("cv", "vac"): return "no_info"
            elif category_name not in (
                "devops", 
                "frontend", 
                "backend"
            ):  
                return "no_info"
            else:
                return "retriever"
        else:
            return "end"
