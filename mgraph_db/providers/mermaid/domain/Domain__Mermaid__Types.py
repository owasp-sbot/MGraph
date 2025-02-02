from typing                                                     import Type
from mgraph_db.mgraph.domain.Domain__MGraph__Types              import Domain__MGraph__Types
from mgraph_db.providers.mermaid.domain.Domain__Mermaid__Edge   import Domain__Mermaid__Edge
from mgraph_db.providers.mermaid.domain.Domain__Mermaid__Node   import Domain__Mermaid__Node

class Domain__Mermaid__Types(Domain__MGraph__Types):
    node_domain_type: Type[Domain__Mermaid__Node]
    edge_domain_type: Type[Domain__Mermaid__Edge]