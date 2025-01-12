from typing                                                   import Type
from mgraph_ai.mgraph.domain.Domain__MGraph__Graph            import Domain__MGraph__Graph
from mgraph_ai.providers.mermaid.domain.Domain__Mermaid__Edge import Domain__Mermaid__Edge
from mgraph_ai.providers.mermaid.domain.Domain__Mermaid__Node import Domain__Mermaid__Node
from mgraph_ai.providers.mermaid.models.Model__Mermaid__Graph import Model__Mermaid__Graph

class Domain__Mermaid__Graph(Domain__MGraph__Graph):
    model           : Model__Mermaid__Graph
    node_domain_type: Type[Domain__Mermaid__Node]
    edge_domain_type: Type[Domain__Mermaid__Edge]
