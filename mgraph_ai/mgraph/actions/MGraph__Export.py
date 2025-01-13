from mgraph_ai.mgraph.actions.MGraph__Data import MGraph__Data
from mgraph_ai.mgraph.domain.Domain__MGraph__Graph import Domain__MGraph__Graph
from osbot_utils.type_safe.Type_Safe               import Type_Safe

class MGraph__Export(Type_Safe):
    graph: Domain__MGraph__Graph

    def data(self):
        return MGraph__Data(graph=self.graph)

    def to__mgraph_json(self):
        return self.graph.model.data.json()

    def to__json(self):
        nodes = {}
        edges = {}
        with self.data() as _:
            for domain_node in _.nodes():
                node = domain_node.node_id
                nodes [node] = {}
            for domain_edge in _.edges():
                edge = domain_edge.edge_id
                edges[edge] = {'from_node_id': domain_edge.from_node_id(),
                                'to_node_id' : domain_edge.to_node_id  ()}


        return dict(nodes=nodes, edges=edges)