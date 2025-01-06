from mgraph_ai.mermaid.schemas.Schema__Mermaid__Edge         import Schema__Mermaid__Edge
from mgraph_ai.mermaid.schemas.Schema__Mermaid__Edge__Config import Schema__Mermaid__Edge__Config
from mgraph_ai.models.Model__MGraph__Attribute               import Model__MGraph__Edge


class Model__Mermaid__Edge(Model__MGraph__Edge):
    data  : Schema__Mermaid__Edge
    config: Schema__Mermaid__Edge__Config