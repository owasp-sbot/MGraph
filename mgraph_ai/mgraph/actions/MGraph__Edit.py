from osbot_utils.helpers.Random_Guid                    import Random_Guid
from osbot_utils.type_safe.Type_Safe                    import Type_Safe
from mgraph_ai.mgraph.domain.MGraph__Edge               import MGraph__Edge
from mgraph_ai.mgraph.domain.MGraph__Graph              import MGraph__Graph

class MGraph__Edit(Type_Safe):
    graph: MGraph__Graph

    def new_node(self, **kwargs):
        return self.graph.new_node(**kwargs)

    def new_edge(self, **kwargs) -> MGraph__Edge:                                                               # Add a new edge between nodes:
        return self.graph.new_edge(**kwargs)

    def delete_node(self, node_id: Random_Guid) -> bool:                                                        # Remove a node and its connected edges
        return self.graph.delete_node(node_id)

    def delete_edge(self, edge_id: Random_Guid) -> bool:                                                        # Remove an edge
        return self.graph.delete_edge(edge_id)

