from mgraph_ai.domain.MGraph__Graph import MGraph__Graph
from osbot_utils.type_safe.Type_Safe                import Type_Safe


class MGraph(Type_Safe):
    graph: MGraph__Graph

    def edges(self):
        return self.graph.edges()

    def nodes(self):
        return self.graph.nodes()


