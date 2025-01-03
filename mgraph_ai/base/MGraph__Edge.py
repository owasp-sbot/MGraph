from typing                             import Dict, Any
from mgraph_ai.base.MGraph__Attribute   import MGraph__Attribute
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.helpers.Random_Guid    import Random_Guid

class MGraph__Edge(Type_Safe):
    attributes    : Dict[Random_Guid, MGraph__Attribute]
    edge_id       : Random_Guid
    from_node_id  : Random_Guid
    from_node_type: type
    to_node_id    : Random_Guid
    to_node_type  : type