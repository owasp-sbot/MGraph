from typing                                                     import Type
from mgraph_ai.mgraph.domain.Domain__MGraph__Types              import Domain__MGraph__Types
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Edge import Domain__MGraph__Json__Edge
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node import Domain__MGraph__Json__Node

class Domain__MGraph__Json__Types(Domain__MGraph__Types):
    node_domain_type : Type[Domain__MGraph__Json__Node]
    edge_domain_type : Type[Domain__MGraph__Json__Edge]