from typing                                                     import List, Dict
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge  import Schema__Mermaid__Edge
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node  import Schema__Mermaid__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph             import Schema__MGraph__Graph
from osbot_utils.helpers.Random_Guid                            import Random_Guid


class Schema__Mermaid__Graph(Schema__MGraph__Graph):
    edges        : Dict[Random_Guid, Schema__Mermaid__Edge]
    mermaid_code : List[str]
    nodes        : Dict[Random_Guid, Schema__Mermaid__Node]
