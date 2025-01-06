from osbot_utils.helpers.Random_Guid import Random_Guid
from osbot_utils.type_safe.Type_Safe import Type_Safe

class Schema__MGraph__Edge_Config(Type_Safe):
    edge_id       : Random_Guid
    from_node_type: type
    to_node_type  : type