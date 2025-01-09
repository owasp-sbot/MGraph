from typing                                                import Dict, Any, Type
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute    import Schema__MGraph__Attribute
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Config import Schema__MGraph__Node__Config
from osbot_utils.helpers.Random_Guid                       import Random_Guid
from osbot_utils.type_safe.Type_Safe                       import Type_Safe

class Schema__MGraph__Node(Type_Safe):
    attributes : Dict[Random_Guid, Schema__MGraph__Attribute]
    node_config: Schema__MGraph__Node__Config
    node_type  : Type['Schema__MGraph__Node']
    value      : Any