from typing                                                 import Dict, Type
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute     import Schema__MGraph__Attribute
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config  import Schema__MGraph__Edge__Config
from osbot_utils.type_safe.Type_Safe                        import Type_Safe
from osbot_utils.helpers.Random_Guid                        import Random_Guid

class Schema__MGraph__Edge(Type_Safe):
    attributes    : Dict[Random_Guid, Schema__MGraph__Attribute]
    edge_config   : Schema__MGraph__Edge__Config
    edge_type     : Type['Schema__MGraph__Edge']
    from_node_id  : Random_Guid
    to_node_id    : Random_Guid