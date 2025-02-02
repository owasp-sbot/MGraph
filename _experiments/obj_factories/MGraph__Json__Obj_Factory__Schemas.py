from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Edge                 import Schema__MGraph__Json__Edge
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Graph                import Schema__MGraph__Json__Graph
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Graph__Data          import Schema__MGraph__Json__Graph__Data
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node                 import Schema__MGraph__Json__Node
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Dict           import Schema__MGraph__Json__Node__Dict
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__List           import Schema__MGraph__Json__Node__List
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Property       import Schema__MGraph__Json__Node__Property
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Property__Data import Schema__MGraph__Json__Node__Property__Data
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value          import Schema__MGraph__Json__Node__Value
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value__Data    import Schema__MGraph__Json__Node__Value__Data
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Types                import Schema__MGraph__Json__Types
from osbot_utils.type_safe.Type_Safe                                             import Type_Safe

class MGraph__Json__Obj_Factory__Schemas(Type_Safe):
    schema_factory: MGraph__Obj_Factory__Schemas

    def __init__(self):
        super().__init__()
        self.schema_factory = MGraph__Obj_Factory__Schemas()

    def create__Schema__MGraph__Json__Node(self):
        node      = object.__new__(Schema__MGraph__Json__Node)
        node_dict = dict(node_data = self.schema_factory.create__Schema__MGraph__Node__Data(),
                         node_id   = self.schema_factory.create__Schema__MGraph__Node().node_id,
                         node_type = Schema__MGraph__Json__Node)
        object.__setattr__(node, '__dict__', node_dict)
        return node

    def create__Schema__MGraph__Json__Node__Value__Data(self):
        data = object.__new__(Schema__MGraph__Json__Node__Value__Data)
        data_dict = dict(value = None,
                        value_type = str)
        object.__setattr__(data, '__dict__', data_dict)
        return data

    def create__Schema__MGraph__Json__Node__Property__Data(self):
        data = object.__new__(Schema__MGraph__Json__Node__Property__Data)
        data_dict = dict(name = '')
        object.__setattr__(data, '__dict__', data_dict)
        return data

    def create__Schema__MGraph__Json__Node__Value(self):
        node = object.__new__(Schema__MGraph__Json__Node__Value)
        node_dict = dict(node_data = self.create__Schema__MGraph__Json__Node__Value__Data(),
                        node_id = self.schema_factory.create__Schema__MGraph__Node().node_id,
                        node_type = Schema__MGraph__Json__Node__Value)
        object.__setattr__(node, '__dict__', node_dict)
        return node

    def create__Schema__MGraph__Json__Node__Property(self):
        node = object.__new__(Schema__MGraph__Json__Node__Property)
        node_dict = dict(node_data = self.create__Schema__MGraph__Json__Node__Property__Data(),
                        node_id = self.schema_factory.create__Schema__MGraph__Node().node_id,
                        node_type = Schema__MGraph__Json__Node__Property)
        object.__setattr__(node, '__dict__', node_dict)
        return node

    def create__Schema__MGraph__Json__Node__Dict(self):
        node = object.__new__(Schema__MGraph__Json__Node__Dict)
        base_node = self.schema_factory.create__Schema__MGraph__Node()
        node_dict = dict(node_data = base_node.node_data,
                        node_id = base_node.node_id,
                        node_type = Schema__MGraph__Json__Node__Dict)
        object.__setattr__(node, '__dict__', node_dict)
        return node

    def create__Schema__MGraph__Json__Node__List(self):
        node = object.__new__(Schema__MGraph__Json__Node__List)
        base_node = self.schema_factory.create__Schema__MGraph__Node()
        node_dict = dict(node_data = base_node.node_data,
                        node_id = base_node.node_id,
                        node_type = Schema__MGraph__Json__Node__List)
        object.__setattr__(node, '__dict__', node_dict)
        return node

    def create__Schema__MGraph__Json__Edge(self):
        edge = object.__new__(Schema__MGraph__Json__Edge)
        base_edge = self.schema_factory.create__Schema__MGraph__Edge()
        edge_dict = dict(edge_config = base_edge.edge_config,
                        edge_data = base_edge.edge_data,
                        edge_type = Schema__MGraph__Json__Edge,
                        from_node_id = base_edge.from_node_id,
                        to_node_id = base_edge.to_node_id)
        object.__setattr__(edge, '__dict__', edge_dict)
        return edge

    def create__Schema__MGraph__Json__Graph__Data(self):
        data = object.__new__(Schema__MGraph__Json__Graph__Data)
        data_dict = dict(root_id = None)
        object.__setattr__(data, '__dict__', data_dict)
        return data

    def create__Schema__MGraph__Json__Types(self):
        types = object.__new__(Schema__MGraph__Json__Types)
        types_dict = dict(edge_type = Schema__MGraph__Json__Edge,
                         edge_config_type = self.schema_factory.create__Schema__MGraph__Edge__Config().__class__,
                         graph_data_type = Schema__MGraph__Json__Graph__Data,
                         node_type = Schema__MGraph__Json__Node,
                         node_data_type = Schema__MGraph__Json__Node__Value__Data)
        object.__setattr__(types, '__dict__', types_dict)
        return types

    def create__Schema__MGraph__Json__Graph(self):
        graph = object.__new__(Schema__MGraph__Json__Graph)
        base_graph = self.schema_factory.create__Schema__MGraph__Graph()
        graph_dict = dict(edges = {},
                         graph_data = self.create__Schema__MGraph__Json__Graph__Data(),
                         graph_id = base_graph.graph_id,
                         graph_type = Schema__MGraph__Json__Graph,
                         nodes = {},
                         schema_types = self.create__Schema__MGraph__Json__Types())
        object.__setattr__(graph, '__dict__', graph_dict)
        return graph