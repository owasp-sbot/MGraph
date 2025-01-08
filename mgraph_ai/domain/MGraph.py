from typing                                         import Any, Dict, Type, List
from mgraph_ai.domain.MGraph__Edge                  import MGraph__Edge
from mgraph_ai.domain.MGraph__Node                  import MGraph__Node
from mgraph_ai.models.Model__MGraph__Edge           import Model__MGraph__Edge
from mgraph_ai.models.Model__MGraph__Graph          import Model__MGraph__Graph
from mgraph_ai.models.Model__MGraph__Node           import Model__MGraph__Node
from mgraph_ai.schemas.Schema__MGraph__Attribute    import Schema__MGraph__Attribute
from mgraph_ai.schemas.Schema__MGraph__Node         import Schema__MGraph__Node
from osbot_utils.helpers.Random_Guid                import Random_Guid
from osbot_utils.type_safe.Type_Safe                import Type_Safe
from osbot_utils.type_safe.decorators.type_safe     import type_safe

class MGraph(Type_Safe):                                                                                        # Main MGraph class that users will interact with
    graph: Model__MGraph__Graph                                                                                 # Reference to the underlying graph model

    @type_safe
    def add_node(self, value     : Any                                                ,
                       node_type : Type[Schema__MGraph__Node                  ] = None,
                       attributes: Dict[Random_Guid, Schema__MGraph__Attribute] = None) -> MGraph__Node:        # Add a new Node

        node = self.graph.new_node(value=value, node_type=node_type, attributes=attributes)
        return self.wrap_node(node)

    @type_safe
    def add_edge(self, from_node_id: Random_Guid,
                       to_node_id  : Random_Guid) -> MGraph__Edge:                                              # Add a new edge between nodes

        edge = self.graph.new_edge(from_node_id=from_node_id, to_node_id=to_node_id)
        return self.wrap_edge(edge)

    def delete_node(self, node_id: Random_Guid) -> bool:                                                        # Remove a node and its connected edges
        return self.graph.delete_node(node_id)

    def delete_edge(self, edge_id: Random_Guid) -> bool:                                                        # Remove an edge
        return self.graph.delete_edge(edge_id)

    def node(self, node_id: Random_Guid) -> MGraph__Node:                                                       # Get a node by its ID
        node = self.graph.get_node(node_id)
        if node:
            return MGraph__Node(node=Model__MGraph__Node(data=node), graph=self.graph)

    def edge(self, edge_id: Random_Guid) -> MGraph__Edge:                                                       # Get an edge by its ID
        edge = self.graph.get_edge(edge_id)
        if edge:
            return MGraph__Edge(edge=Model__MGraph__Edge(data=edge), graph=self.graph)

    def edges(self) -> List[MGraph__Edge]:                                                                      # Get all edges in the graph
        return [self.wrap_edge(edge) for edge in self.graph.edges()]

    def nodes(self) -> List[MGraph__Node]:                                                                      # Get all nodes in the graph
        return [self.wrap_node(node) for node in self.graph.nodes()]


