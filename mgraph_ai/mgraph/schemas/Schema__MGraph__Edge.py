from typing                                                 import Dict, Type
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config  import Schema__MGraph__Edge__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Data import Schema__MGraph__Edge__Data
from osbot_utils.type_safe.Type_Safe                        import Type_Safe
from osbot_utils.helpers.Random_Guid                        import Random_Guid

class Schema__MGraph__Edge(Type_Safe):
    edge_config   : Schema__MGraph__Edge__Config
    edge_data     : Schema__MGraph__Edge__Data
    edge_type     : Type['Schema__MGraph__Edge']
    from_node_id  : Random_Guid
    to_node_id    : Random_Guid