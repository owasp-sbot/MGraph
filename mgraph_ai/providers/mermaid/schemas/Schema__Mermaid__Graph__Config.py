from typing                                                     import Type
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph_Config      import Schema__MGraph__Graph_Config
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge  import Schema__Mermaid__Edge
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node  import Schema__Mermaid__Node


class Schema__Mermaid__Graph__Config(Schema__MGraph__Graph_Config):
    default_edge_type     : Type[Schema__Mermaid__Edge]
    default_node_type     : Type[Schema__Mermaid__Node]
    allow_circle_edges    : bool
    allow_duplicate_edges : bool
    graph_title           : str