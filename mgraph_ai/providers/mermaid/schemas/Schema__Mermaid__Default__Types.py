from typing                                                             import Type
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute                 import Schema__MGraph__Attribute
from mgraph_ai.mgraph.schemas.Schema__MGraph__Default__Types            import Schema__MGraph__Default__Types
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge          import Schema__Mermaid__Edge
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge__Config  import Schema__Mermaid__Edge__Config
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Graph__Config import Schema__Mermaid__Graph__Config
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node          import Schema__Mermaid__Node
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Config  import Schema__Mermaid__Node__Config

class Schema__Mermaid__Default__Types(Schema__MGraph__Default__Types):
    attribute_type   : Type[Schema__MGraph__Attribute     ]                     # todo: remove when bug in Type_Safe is fixed
    edge_type        : Type[Schema__Mermaid__Edge         ]
    edge_config_type : Type[Schema__Mermaid__Edge__Config ]
    graph_config_type: Type[Schema__Mermaid__Graph__Config]
    node_type        : Type[Schema__Mermaid__Node         ]
    node_config_type : Type[Schema__Mermaid__Node__Config ]
