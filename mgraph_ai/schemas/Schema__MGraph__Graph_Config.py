from osbot_utils.helpers.Random_Guid import Random_Guid
from osbot_utils.type_safe.Type_Safe import Type_Safe


class Schema__MGraph__Graph_Config(Type_Safe):
    default_edge_type: type
    default_node_type: type
    graph_id         : Random_Guid
    graph_type       : type