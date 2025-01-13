from mgraph_ai.mgraph.domain.Domain__MGraph__Graph import Domain__MGraph__Graph
from osbot_utils.type_safe.Type_Safe               import Type_Safe

class MGraph__Export(Type_Safe):
    graph: Domain__MGraph__Graph

    def to__mgraph_json(self):
        return self.graph.model.data.json()