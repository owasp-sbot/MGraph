from typing                                             import Any, Type, Dict, List
from osbot_utils.helpers.Random_Guid                    import Random_Guid
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute import Schema__MGraph__Attribute
from mgraph_ai.mgraph.domain.MGraph__Edge               import MGraph__Edge
from mgraph_ai.mgraph.domain.MGraph__Node               import MGraph__Node
from mgraph_ai.mgraph.models.Model__MGraph__Graph       import Model__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node      import Schema__MGraph__Node
from osbot_utils.type_safe.Type_Safe                    import Type_Safe


class MGraph__Graph(Type_Safe):
    graph: Model__MGraph__Graph

    def delete_edge(self, edge_id: Random_Guid) -> bool:
        return self.graph.delete_edge(edge_id)

    def delete_node(self, node_id: Random_Guid) -> bool:
        return self.graph.delete_node(node_id)

    def edge(self, edge_id: Random_Guid) -> MGraph__Edge:
        edge = self.graph.edge(edge_id)
        if edge:
            return MGraph__Edge(edge=edge, graph=self.graph)

    def edges(self) -> List[MGraph__Edge]:
        return [MGraph__Edge(edge=edge, graph=self.graph) for edge in self.graph.edges()]

    def new_edge(self, from_node_id: Random_Guid, to_node_id  : Random_Guid) -> MGraph__Edge:
        edge = self.graph.new_edge(from_node_id=from_node_id, to_node_id=to_node_id)
        return MGraph__Edge(edge=edge, graph=self.graph)

    def new_node(self, value     : Any                                                ,
                       node_type : Type[Schema__MGraph__Node                  ] = None,
                       attributes: Dict[Random_Guid, Schema__MGraph__Attribute] = None)-> MGraph__Node:
        node = self.graph.new_node(value=value, node_type=node_type, attributes=attributes)
        return MGraph__Node(node=node, graph=self.graph)

    def node(self, node_id: Random_Guid) -> MGraph__Node:
        node = self.graph.node(node_id)
        if node:
            return MGraph__Node(node=node, graph=self.graph)

    def nodes(self) -> List[MGraph__Node]:
        return [MGraph__Node(node=node, graph=self.graph) for node in self.graph.nodes()]

