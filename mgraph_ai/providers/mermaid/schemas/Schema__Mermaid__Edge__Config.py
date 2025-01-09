from typing                                                    import Type
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge_Config      import Schema__MGraph__Edge_Config
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node import Schema__Mermaid__Node


class Schema__Mermaid__Edge__Config(Schema__MGraph__Edge_Config):
    from_node_type: Type[Schema__Mermaid__Node]
    to_node_type  : Type[Schema__Mermaid__Node]