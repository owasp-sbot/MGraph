from typing                                         import Type
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node  import Schema__MGraph__Node
from osbot_utils.helpers.Random_Guid                import Random_Guid
from osbot_utils.type_safe.Type_Safe                import Type_Safe

class Schema__MGraph__Edge__Config(Type_Safe):
    edge_id       : Random_Guid
    from_node_type: Type[Schema__MGraph__Node]
    to_node_type  : Type[Schema__MGraph__Node]