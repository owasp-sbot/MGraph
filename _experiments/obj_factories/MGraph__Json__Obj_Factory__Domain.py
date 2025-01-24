from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Edge            import Domain__MGraph__Json__Edge
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Graph           import Domain__MGraph__Json__Graph
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node            import Domain__MGraph__Json__Node
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node__Dict      import Domain__MGraph__Json__Node__Dict
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node__List      import Domain__MGraph__Json__Node__List
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node__Property  import Domain__MGraph__Json__Node__Property
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node__Value     import Domain__MGraph__Json__Node__Value
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Types           import Domain__MGraph__Json__Types
from mgraph_ai.providers.json.actions.MGraph__Json__Obj_Factory__Models    import MGraph__Json__Obj_Factory__Models
from osbot_utils.type_safe.Type_Safe                                       import Type_Safe

class MGraph__Json__Obj_Factory__Domain(Type_Safe):
    json_models_factory: MGraph__Json__Obj_Factory__Models

    def __init__(self):
        super().__init__()
        self.json_models_factory = MGraph__Json__Obj_Factory__Models()

    def create__Domain__MGraph__Json__Types(self):
        types = object.__new__(Domain__MGraph__Json__Types)
        types_dict = dict(node_domain_type = Domain__MGraph__Json__Node,
                         edge_domain_type = Domain__MGraph__Json__Edge)
        object.__setattr__(types, '__dict__', types_dict)
        return types

    def create__Domain__MGraph__Json__Node__Value(self):
        node = object.__new__(Domain__MGraph__Json__Node__Value)
        node_dict = dict(node = self.json_models_factory.create__Model__MGraph__Json__Node__Value(),
                        graph = self.json_models_factory.create__Model__MGraph__Json__Graph())
        object.__setattr__(node, '__dict__', node_dict)
        return node

    def create__Domain__MGraph__Json__Node__Property(self):
        node = object.__new__(Domain__MGraph__Json__Node__Property)
        node_dict = dict(node = self.json_models_factory.create__Model__MGraph__Json__Node__Property(),
                        graph = self.json_models_factory.create__Model__MGraph__Json__Graph())
        object.__setattr__(node, '__dict__', node_dict)
        return node

    def create__Domain__MGraph__Json__Node__Dict(self):
        node = object.__new__(Domain__MGraph__Json__Node__Dict)
        node_dict = dict(node = self.json_models_factory.create__Model__MGraph__Json__Node__Dict(),
                        graph = self.json_models_factory.create__Model__MGraph__Json__Graph())
        object.__setattr__(node, '__dict__', node_dict)
        return node

    def create__Domain__MGraph__Json__Node__List(self):
        node = object.__new__(Domain__MGraph__Json__Node__List)
        node_dict = dict(node = self.json_models_factory.create__Model__MGraph__Json__Node__List(),
                        graph = self.json_models_factory.create__Model__MGraph__Json__Graph())
        object.__setattr__(node, '__dict__', node_dict)
        return node

    def create__Domain__MGraph__Json__Edge(self):
        edge = object.__new__(Domain__MGraph__Json__Edge)
        edge_dict = dict(edge = self.json_models_factory.create__Model__MGraph__Json__Edge(),
                        graph = self.json_models_factory.create__Model__MGraph__Json__Graph())
        object.__setattr__(edge, '__dict__', edge_dict)
        return edge

    def create__Domain__MGraph__Json__Graph(self):
        graph = object.__new__(Domain__MGraph__Json__Graph)
        graph_dict = dict(domain_types = self.create__Domain__MGraph__Json__Types(),
                         model = self.json_models_factory.create__Model__MGraph__Json__Graph())
        object.__setattr__(graph, '__dict__', graph_dict)
        return graph