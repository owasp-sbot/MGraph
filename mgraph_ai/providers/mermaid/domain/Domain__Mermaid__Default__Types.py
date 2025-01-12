from typing                                                   import Type
from mgraph_ai.mgraph.domain.Domain__MGraph__Default__Types   import Domain__MGraph__Default__Types
from mgraph_ai.providers.mermaid.domain.Domain__Mermaid__Edge import Domain__Mermaid__Edge
from mgraph_ai.providers.mermaid.domain.Domain__Mermaid__Node import Domain__Mermaid__Node

class Domain__Mermaid__Default__Types(Domain__MGraph__Default__Types):
    node_domain_type: Type[Domain__Mermaid__Node]
    edge_domain_type: Type[Domain__Mermaid__Edge]