from typing                                                              import List, Dict, Type

from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Render__Config import Schema__Mermaid__Render__Config
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Default__Types import Schema__Mermaid__Default__Types
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge           import Schema__Mermaid__Edge
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Graph__Config  import Schema__Mermaid__Graph__Config
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node           import Schema__Mermaid__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph                      import Schema__MGraph__Graph
from osbot_utils.helpers.Random_Guid                                     import Random_Guid


class Schema__Mermaid__Graph(Schema__MGraph__Graph):
    default_types: Schema__Mermaid__Default__Types
    edges        : Dict[Random_Guid, Schema__Mermaid__Edge]
    graph_config : Schema__Mermaid__Graph__Config
    graph_type   : Type['Schema__Mermaid__Graph']
    mermaid_code : List[str]
    nodes        : Dict[Random_Guid, Schema__Mermaid__Node]
    render_config: Schema__Mermaid__Render__Config

