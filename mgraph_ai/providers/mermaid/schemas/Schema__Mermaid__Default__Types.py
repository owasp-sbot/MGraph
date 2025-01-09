from typing                                                             import Type
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge          import Schema__Mermaid__Edge
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge__Config  import Schema__Mermaid__Edge__Config
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Graph__Config import Schema__Mermaid__Graph__Config
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node          import Schema__Mermaid__Node
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Config  import Schema__Mermaid__Node__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute                 import Schema__MGraph__Attribute

class Schema__Mermaid__Default__Types(Type_Safe):
    attribute_type   : Type[Schema__MGraph__Attribute     ]
    edge_type        : Type[Schema__Mermaid__Edge         ]
    edge_config_type : Type[Schema__Mermaid__Edge__Config ]
    graph_config_type: Type[Schema__Mermaid__Graph__Config]
    node_type        : Type[Schema__Mermaid__Node         ]
    node_config_type : Type[Schema__Mermaid__Node__Config ]