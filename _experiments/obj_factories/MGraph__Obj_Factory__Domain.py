from mgraph_ai.mgraph.domain.Domain__MGraph__Edge      import Domain__MGraph__Edge
from mgraph_ai.mgraph.domain.Domain__MGraph__Graph     import Domain__MGraph__Graph
from mgraph_ai.mgraph.domain.Domain__MGraph__Node      import Domain__MGraph__Node
from mgraph_ai.mgraph.domain.Domain__MGraph__Types     import Domain__MGraph__Types
from mgraph_ai.mgraph.actions.MGraph__Obj_Factory__Models import MGraph__Obj_Factory__Models
from osbot_utils.type_safe.Type_Safe                   import Type_Safe

class MGraph__Obj_Factory__Domain(Type_Safe):
    models_factory: MGraph__Obj_Factory__Models

    def __init__(self):
        super().__init__()
        self.models_factory = MGraph__Obj_Factory__Models()

    def create__Domain__MGraph__Types(self):
        types = object.__new__(Domain__MGraph__Types)
        types_dict = dict(node_domain_type = Domain__MGraph__Node,
                         edge_domain_type = Domain__MGraph__Edge)
        object.__setattr__(types, '__dict__', types_dict)
        return types

    def create__Domain__MGraph__Node(self):
        node = object.__new__(Domain__MGraph__Node)
        node_dict = dict(node = self.models_factory.create__Model__MGraph__Node(),
                        graph = self.models_factory.create__Model__MGraph__Graph())
        object.__setattr__(node, '__dict__', node_dict)
        return node

    def create__Domain__MGraph__Edge(self):
        edge = object.__new__(Domain__MGraph__Edge)
        edge_dict = dict(edge = self.models_factory.create__Model__MGraph__Edge(),
                        graph = self.models_factory.create__Model__MGraph__Graph())
        object.__setattr__(edge, '__dict__', edge_dict)
        return edge

    def create__Domain__MGraph__Graph(self):
        graph = object.__new__(Domain__MGraph__Graph)
        graph_dict = dict(domain_types = self.create__Domain__MGraph__Types(),
                         model = self.models_factory.create__Model__MGraph__Graph())
        object.__setattr__(graph, '__dict__', graph_dict)
        return graph