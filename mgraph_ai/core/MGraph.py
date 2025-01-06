from mgraph_ai.mermaid.models.Model__Mermaid__Graph import Model__Mermaid__Graph
from mgraph_ai.schemas.Schema__MGraph__Edge  import Schema__MGraph__Edge
from mgraph_ai.schemas.Schema__MGraph__Node  import Schema__MGraph__Node
from osbot_utils.type_safe.Type_Safe         import Type_Safe

# todo add support for storing the data in sqlite so that we get the ability to search nodes and edges
class MGraph(Type_Safe):
    model: Model__Mermaid__Graph

    def add_edge(self, from_node_id, to_node_id, attributes=None) -> Schema__MGraph__Edge:
        # if self.config.allow_circle_edges is False:                           # these checks should not exist in the core
        #     if from_node_id == to_node_id:
        #         return None
        # if self.config.allow_duplicate_edges is False:                          # todo: figure out if there is a more efficient way to do this
        #     for edge in self.edges():
        #         if edge.from_node_id == from_node_id and edge.to_node_id == to_node_id:
        #             return None
        new_edge = Schema__MGraph__Edge(from_node_id=from_node_id, to_node_id=to_node_id, attributes=attributes)
        self.data.edges[new_edge.edge_id] = new_edge
        return new_edge

    def add_node(self, **kwargs):
        return self.model.add_node(**kwargs)

    def edges(self):
        return self.data.edges

    def node(self, node_id):
        return self.nodes().get(node_id)

    def nodes(self):
        return self.data.nodes

    def new_node(self):
        new_node = Schema__MGraph__Node()
        return self.add_node(new_node)