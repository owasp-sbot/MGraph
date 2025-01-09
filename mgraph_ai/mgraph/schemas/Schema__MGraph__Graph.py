from typing                                                  import Dict, Type
from mgraph_ai.mgraph.schemas.Schema__MGraph__Default__Types import Schema__MGraph__Default__Types
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge           import Schema__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph__Config  import Schema__MGraph__Graph__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node           import Schema__MGraph__Node
from osbot_utils.type_safe.Type_Safe                         import Type_Safe
from osbot_utils.helpers.Random_Guid                         import Random_Guid

class Schema__MGraph__Graph(Type_Safe):
    default_types: Schema__MGraph__Default__Types
    edges        : Dict[Random_Guid, Schema__MGraph__Edge]
    graph_config : Schema__MGraph__Graph__Config
    graph_type   : Type['Schema__MGraph__Graph']
    nodes        : Dict[Random_Guid, Schema__MGraph__Node]
