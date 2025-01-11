from typing                                 import List
from mgraph_ai.mgraph.domain.MGraph__Edge   import MGraph__Edge
from mgraph_ai.mgraph.domain.MGraph__Graph  import MGraph__Graph
from mgraph_ai.mgraph.domain.MGraph__Node   import MGraph__Node
from osbot_utils.helpers                    import Random_Guid
from osbot_utils.type_safe.Type_Safe        import Type_Safe

class MGraph__Data(Type_Safe):
    graph: MGraph__Graph

    def node(self, node_id: Random_Guid) -> MGraph__Node:                                                               # Get a node by its ID
        return self.graph.node(node_id)

    def edge(self, edge_id: Random_Guid) -> MGraph__Edge:                                                               # Get an edge by its ID
        return self.graph.edge(edge_id)

    def edges(self) -> List[MGraph__Edge]:                                                                              # Get all edges in the graph
        return self.graph.edges()

    def graph_id(self):
        return self.graph.graph_id()

    def nodes(self) -> List[MGraph__Node]:                                                                              # Get all nodes in the graph
        return self.graph.nodes()