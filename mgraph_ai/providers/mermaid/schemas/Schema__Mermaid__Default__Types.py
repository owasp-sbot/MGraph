from typing                                                             import Type
from mgraph_ai.mgraph.schemas.Schema__MGraph__Default__Types            import Schema__MGraph__Default__Types
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge          import Schema__Mermaid__Edge
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge__Config  import Schema__Mermaid__Edge__Config
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Graph__Config import Schema__Mermaid__Graph__Config
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node          import Schema__Mermaid__Node
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Data    import Schema__Mermaid__Node__Data

class Schema__Mermaid__Default__Types(Schema__MGraph__Default__Types):
    edge_type        : Type[Schema__Mermaid__Edge         ]
    edge_config_type : Type[Schema__Mermaid__Edge__Config ]
    graph_config_type: Type[Schema__Mermaid__Graph__Config]
    node_type        : Type[Schema__Mermaid__Node         ]
    node_data_type : Type[Schema__Mermaid__Node__Data]
