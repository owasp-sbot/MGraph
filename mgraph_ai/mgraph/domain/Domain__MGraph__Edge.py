from typing                                                import Any, List
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config import Schema__MGraph__Edge__Config
from osbot_utils.helpers.Random_Guid                       import Random_Guid
from osbot_utils.helpers.Safe_Id                           import Safe_Id
from mgraph_ai.mgraph.domain.Domain__MGraph__Node          import Domain__MGraph__Node
from mgraph_ai.mgraph.models.Model__MGraph__Edge           import Model__MGraph__Edge
from mgraph_ai.mgraph.models.Model__MGraph__Graph          import Model__MGraph__Graph
from osbot_utils.type_safe.Type_Safe                       import Type_Safe
from osbot_utils.type_safe.methods.type_safe_property      import set_as_property


class Domain__MGraph__Edge(Type_Safe):                                                                  # Domain class for edges
    edge : Model__MGraph__Edge                                                                          # Reference to edge model
    graph: Model__MGraph__Graph                                                                         # Reference to graph model

    edge_config = set_as_property('edge.data'            , 'edge_config', Schema__MGraph__Edge__Config) # Edge configuration
    edge_id     = set_as_property('edge.data.edge_config', 'edge_id'    , Random_Guid                 ) # Edge ID

    def from_node(self) -> Domain__MGraph__Node:                                                        # Get source node
        node = self.graph.node(self.edge.from_node_id())
        if node:
            return Domain__MGraph__Node(node=node, graph=self.graph)

    def to_node(self) -> Domain__MGraph__Node:                                                          # Get target node
        node = self.graph.node(self.edge.to_node_id())
        if node:
            return Domain__MGraph__Node(node=node, graph=self.graph)