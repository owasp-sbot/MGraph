from typing                                                   import Type
from mgraph_ai.mgraph.domain.MGraph__Graph                    import MGraph__Graph
from mgraph_ai.providers.mermaid.domain.Mermaid__Edge         import Mermaid__Edge
from mgraph_ai.providers.mermaid.domain.Mermaid__Node         import Mermaid__Node
from mgraph_ai.providers.mermaid.models.Model__Mermaid__Graph import Model__Mermaid__Graph

class Mermaid__Graph(MGraph__Graph):
    model           : Model__Mermaid__Graph
    node_domain_type: Type[Mermaid__Node]
    edge_domain_type: Type[Mermaid__Edge]
