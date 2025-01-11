from typing                                                 import Type
from osbot_utils.type_safe.Type_Safe                        import Type_Safe
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute     import Schema__MGraph__Attribute
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge          import Schema__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config  import Schema__MGraph__Edge__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph__Config import Schema__MGraph__Graph__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node          import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Config  import Schema__MGraph__Node__Config

class Schema__MGraph__Default__Types(Type_Safe):
    attribute_type   : Type[Schema__MGraph__Attribute    ]
    edge_type        : Type[Schema__MGraph__Edge         ]
    edge_config_type : Type[Schema__MGraph__Edge__Config ]
    graph_config_type: Type[Schema__MGraph__Graph__Config]
    node_type        : Type[Schema__MGraph__Node         ]
    node_config_type : Type[Schema__MGraph__Node__Config ]
