from typing                                 import List
from mgraph_ai.domain.MGraph__Edge          import MGraph__Edge
from mgraph_ai.domain.MGraph__Graph         import MGraph__Graph
from mgraph_ai.domain.MGraph__Node          import MGraph__Node
from mgraph_ai.models.Model__MGraph__Edge   import Model__MGraph__Edge
from mgraph_ai.models.Model__MGraph__Node   import Model__MGraph__Node
from osbot_utils.helpers                    import Random_Guid
from osbot_utils.type_safe.Type_Safe        import Type_Safe

class MGraph__Data(Type_Safe):
    graph: MGraph__Graph

    def node(self, node_id: Random_Guid) -> MGraph__Node:                                                               # Get a node by its ID
        node = self.graph.node(node_id)
        if node:
            return MGraph__Node(node=Model__MGraph__Node(data=node), graph=self.graph)

    def edge(self, edge_id: Random_Guid) -> MGraph__Edge:                                                               # Get an edge by its ID
        edge = self.graph.edge(edge_id)
        if edge:
            return MGraph__Edge(edge=Model__MGraph__Edge(data=edge), graph=self.graph)

    def edges(self) -> List[MGraph__Edge]:                                                                              # Get all edges in the graph
        return [MGraph__Edge(edge=Model__MGraph__Edge(data=edge), graph=self.graph) for edge in self.graph.edges()]

    def nodes(self) -> List[MGraph__Node]:                                                                              # Get all nodes in the graph
        return [MGraph__Node(node=Model__MGraph__Node(data=node), graph=self.graph) for node in self.graph.nodes()]