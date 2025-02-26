from typing                                                 import Type

from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Edge import Schema__MGraph__Json__Edge
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node import Schema__MGraph__Json__Node
from osbot_utils.type_safe.Type_Safe                        import Type_Safe
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data   import Schema__MGraph__Graph__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data    import Schema__MGraph__Node__Data

class Schema__MGraph__Json__Types(Type_Safe):
    edge_type        : Type[Schema__MGraph__Json__Edge   ]
    graph_data_type  : Type[Schema__MGraph__Graph__Data  ]
    node_type        : Type[Schema__MGraph__Json__Node   ]
    node_data_type   : Type[Schema__MGraph__Node__Data   ]

    def __init__(self, **kwargs):
        edge_type        = kwargs.get('edge_type'       ) or self.__annotations__['edge_type'].__args__[0]
        graph_data_type  = kwargs.get('graph_data_type' ) or self.__annotations__['graph_data_type'].__args__[0]
        node_type        = kwargs.get('node_type'       ) or self.__annotations__['node_type'].__args__[0]
        node_data_type   = kwargs.get('node_data_type'  ) or self.__annotations__['node_data_type'].__args__[0]

        types_dict = dict(edge_type        = edge_type       ,
                          graph_data_type  = graph_data_type ,
                          node_type        = node_type       ,
                          node_data_type   = node_data_type  )
        object.__setattr__(self, '__dict__', types_dict)
