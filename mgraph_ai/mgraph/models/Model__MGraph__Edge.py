from osbot_utils.helpers.Random_Guid                       import Random_Guid
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config import Schema__MGraph__Edge__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge         import Schema__MGraph__Edge
from osbot_utils.type_safe.Type_Safe                       import Type_Safe


class Model__MGraph__Edge(Type_Safe):
    data: Schema__MGraph__Edge

    def from_node_id(self) -> Random_Guid:
        return self.data.from_node_id

    def edge_config(self) -> Schema__MGraph__Edge__Config:
        return self.data.edge_config

    def edge_id(self) -> Random_Guid:
        return self.edge_config().edge_id

    def to_node_id(self) -> Random_Guid:
        return self.data.to_node_id