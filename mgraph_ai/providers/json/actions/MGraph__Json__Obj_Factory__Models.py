from mgraph_ai.providers.json.models.Model__MGraph__Json__Edge         import Model__MGraph__Json__Edge
from mgraph_ai.providers.json.models.Model__MGraph__Json__Graph        import Model__MGraph__Json__Graph
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node         import Model__MGraph__Json__Node
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node__Dict   import Model__MGraph__Json__Node__Dict
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node__List   import Model__MGraph__Json__Node__List
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node__Property import Model__MGraph__Json__Node__Property
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node__Value  import Model__MGraph__Json__Node__Value
from mgraph_ai.providers.json.models.Model__MGraph__Json__Types        import Model__MGraph__Json__Types
from mgraph_ai.providers.json.actions.MGraph__Json__Obj_Factory__Schemas import MGraph__Json__Obj_Factory__Schemas
from osbot_utils.type_safe.Type_Safe                                   import Type_Safe

class MGraph__Json__Obj_Factory__Models(Type_Safe):
    json_schema_factory: MGraph__Json__Obj_Factory__Schemas

    def __init__(self):
        super().__init__()
        self.json_schema_factory = MGraph__Json__Obj_Factory__Schemas()

    def create__Model__MGraph__Json__Types(self):
        types = object.__new__(Model__MGraph__Json__Types)
        types_dict = dict(node_model_type = Model__MGraph__Json__Node,
                         edge_model_type = Model__MGraph__Json__Edge)
        object.__setattr__(types, '__dict__', types_dict)
        return types

    def create__Model__MGraph__Json__Node(self, data=None):
        node      = object.__new__(Model__MGraph__Json__Node)
        node_dict = dict(data = data or self.json_schema_factory.create__Schema__MGraph__Json__Node())
        object.__setattr__(node, '__dict__', node_dict)
        return node

    def create__Model__MGraph__Json__Node__Value(self):
        node = object.__new__(Model__MGraph__Json__Node__Value)
        node_dict = dict(data = self.json_schema_factory.create__Schema__MGraph__Json__Node__Value())
        object.__setattr__(node, '__dict__', node_dict)
        return node

    def create__Model__MGraph__Json__Node__Property(self):
        node = object.__new__(Model__MGraph__Json__Node__Property)
        node_dict = dict(data = self.json_schema_factory.create__Schema__MGraph__Json__Node__Property())
        object.__setattr__(node, '__dict__', node_dict)
        return node

    def create__Model__MGraph__Json__Node__Dict(self):
        node = object.__new__(Model__MGraph__Json__Node__Dict)
        node_dict = dict(data = self.json_schema_factory.create__Schema__MGraph__Json__Node__Dict())
        object.__setattr__(node, '__dict__', node_dict)
        return node

    def create__Model__MGraph__Json__Node__List(self):
        node = object.__new__(Model__MGraph__Json__Node__List)
        node_dict = dict(data = self.json_schema_factory.create__Schema__MGraph__Json__Node__List())
        object.__setattr__(node, '__dict__', node_dict)
        return node

    def create__Model__MGraph__Json__Edge(self):
        edge = object.__new__(Model__MGraph__Json__Edge)
        edge_dict = dict(data = self.json_schema_factory.create__Schema__MGraph__Json__Edge())
        object.__setattr__(edge, '__dict__', edge_dict)
        return edge

    def create__Model__MGraph__Json__Graph(self):
        graph = object.__new__(Model__MGraph__Json__Graph)
        graph_dict = dict(data = self.json_schema_factory.create__Schema__MGraph__Json__Graph(),
                         model_types = self.create__Model__MGraph__Json__Types())
        object.__setattr__(graph, '__dict__', graph_dict)
        return graph