from typing                                             import Type, Any, List
from osbot_utils.type_safe.Type_Safe                    import Type_Safe
from osbot_utils.helpers.Random_Guid                    import Random_Guid
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node      import Schema__MGraph__Node
from osbot_utils.type_safe.methods.type_safe_property   import set_as_property


class Model__MGraph__Node(Type_Safe):
    data: Schema__MGraph__Node

    node_id   = set_as_property('data.node_data', 'node_id'  , Random_Guid)
    node_type = set_as_property('data'          , 'node_type'             ) # BUG: , Type[Schema__MGraph__Node] not supported, raises "Subscripted generics cannot be used with class and instance checks" error
