from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge import Schema__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node import Schema__MGraph__Node
from osbot_utils.helpers.Obj_Id                    import Obj_Id
from osbot_utils.type_safe.Type_Safe               import Type_Safe
from mgraph_ai.mgraph.domain.Domain__MGraph__Edge  import Domain__MGraph__Edge
from mgraph_ai.mgraph.domain.Domain__MGraph__Graph import Domain__MGraph__Graph

class MGraph__Edit(Type_Safe):
    graph: Domain__MGraph__Graph

    def add_node(self, node: Schema__MGraph__Node):
        return self.graph.add_node(node)

    def new_node(self, **kwargs):
        return self.graph.new_node(**kwargs)

    def add_edge(self, edge: Schema__MGraph__Edge):
        return self.graph.add_edge(edge)

    def new_edge(self, **kwargs) -> Domain__MGraph__Edge:                                                               # Add a new edge between nodes:
        return self.graph.new_edge(**kwargs)

    def delete_node(self, node_id: Obj_Id) -> bool:                                                        # Remove a node and its connected edges
        return self.graph.delete_node(node_id)

    def delete_edge(self, edge_id: Obj_Id) -> bool:                                                        # Remove an edge
        return self.graph.delete_edge(edge_id)

