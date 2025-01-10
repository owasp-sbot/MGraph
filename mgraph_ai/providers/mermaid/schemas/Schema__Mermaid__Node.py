from typing                                                             import Type
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Config  import Schema__Mermaid__Node__Config
from osbot_utils.helpers.Safe_Id                                        import Safe_Id
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node                      import Schema__MGraph__Node

class Schema__Mermaid__Node(Schema__MGraph__Node):
    key        : Safe_Id
    label      : str
    node_config: Schema__Mermaid__Node__Config
    node_type  : Type['Schema__Mermaid__Node']