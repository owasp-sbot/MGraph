from typing                                       import Dict, Any
from mgraph_ai.schemas.Schema__MGraph__Attribute  import Schema__MGraph__Attribute
from osbot_utils.type_safe.Type_Safe              import Type_Safe
from osbot_utils.helpers.Random_Guid              import Random_Guid

class Schema__MGraph__Edge(Type_Safe):
    attributes    : Dict[Random_Guid, Schema__MGraph__Attribute]
    edge_id       : Random_Guid
    from_node_id  : Random_Guid
    from_node_type: type
    to_node_id    : Random_Guid
    to_node_type  : type