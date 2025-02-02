from typing                                                  import Type
from mgraph_db.mgraph.models.Model__MGraph__Types            import Model__MGraph__Types
from mgraph_db.providers.mermaid.models.Model__Mermaid__Edge import Model__Mermaid__Edge
from mgraph_db.providers.mermaid.models.Model__Mermaid__Node import Model__Mermaid__Node


class Model__Mermaid__Types(Model__MGraph__Types):
    node_model_type: Type[Model__Mermaid__Node]
    edge_model_type: Type[Model__Mermaid__Edge]