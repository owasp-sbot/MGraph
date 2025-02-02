from typing                                                     import Type
from mgraph_db.mgraph.domain.Domain__MGraph__Types              import Domain__MGraph__Types
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Edge import Domain__MGraph__Json__Edge
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node import Domain__MGraph__Json__Node

class Domain__MGraph__Json__Types(Domain__MGraph__Types):
    node_domain_type : Type[Domain__MGraph__Json__Node]
    edge_domain_type : Type[Domain__MGraph__Json__Edge]

    # def __init__(self, **kwargs):
    #     node_domain_type = kwargs.get('node_domain_type') or self.__annotations__['node_domain_type'].__args__[0]
    #     edge_domain_type = kwargs.get('edge_domain_type') or self.__annotations__['edge_domain_type'].__args__[0]
    #
    #     types_dict = dict(node_domain_type = node_domain_type,
    #                       edge_domain_type = edge_domain_type)
    #     object.__setattr__(self, '__dict__', types_dict)