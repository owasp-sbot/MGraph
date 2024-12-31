from typing import List, Dict

from osbot_utils.helpers.Random_Guid import Random_Guid

from mgraph_ai.mermaid.Mermaid__Edge    import Mermaid__Edge
from mgraph_ai.mermaid.Mermaid__Node    import Mermaid__Node
from mgraph_ai.core.MGraph              import MGraph


class Mermaid__Graph(MGraph):
    edges        : List[Mermaid__Edge]
    mermaid_code : List
    nodes        : Dict[Random_Guid, Mermaid__Node]
