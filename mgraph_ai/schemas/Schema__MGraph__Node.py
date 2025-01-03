from typing                                         import Dict, Any
from mgraph_ai.schemas.Schema__MGraph__Attribute    import Schema__MGraph__Attribute
from osbot_utils.helpers.Random_Guid                import Random_Guid
from osbot_utils.type_safe.Type_Safe             import Type_Safe

class Schema__MGraph__Node(Type_Safe):
    attributes: Dict[Random_Guid, Schema__MGraph__Attribute]
    node_id   : Random_Guid
    node_type : type