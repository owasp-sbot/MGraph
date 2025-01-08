from mgraph_ai.domain.MGraph__Edge import MGraph__Edge
from mgraph_ai.domain.MGraph__Node import MGraph__Node
from mgraph_ai.models.Model__MGraph__Graph  import Model__MGraph__Graph
from mgraph_ai.schemas.Schema__MGraph__Node import Schema__MGraph__Node
from osbot_utils.type_safe.Type_Safe        import Type_Safe


class MGraph__Graph(Type_Safe):
    graph: Model__MGraph__Graph

    def add_node(self, **kwargs)-> MGraph__Node:
        node = self.model.add_node(**kwargs)
        return MGraph__Node(node=node, graph=self)

    def node(self, node_id) -> MGraph__Node:
        node_model = self.graph.data.nodes.get(node_id)
        return MGraph__Node(node=node_model, graph=self)

    def nodes(self):
        return [MGraph__Node(node=node, graph=self) for node in self.graph.nodes()]

    def edge(self, edge_id):
        edge_model = self.graph.nodes().get(edge_id)
        return MGraph__Edge(edge=edge_model, graph=self)

    def edges(self):
        return [MGraph__Edge(edge=edge, graph=self) for edge in self.graph.edges()]

    def new_node(self):
        node =  Schema__MGraph__Node
        return self.add_node(node=node)