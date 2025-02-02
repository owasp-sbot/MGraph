from mgraph_db.mgraph.actions.MGraph__Obj_Factory__Schemas  import MGraph__Obj_Factory__Schemas
from mgraph_db.mgraph.models.Model__MGraph__Edge            import Model__MGraph__Edge
from mgraph_db.mgraph.models.Model__MGraph__Graph           import Model__MGraph__Graph
from mgraph_db.mgraph.models.Model__MGraph__Node            import Model__MGraph__Node
from mgraph_db.mgraph.models.Model__MGraph__Types           import Model__MGraph__Types
from osbot_utils.type_safe.Type_Safe                        import Type_Safe

class MGraph__Obj_Factory__Models(Type_Safe):
    schema_factory: MGraph__Obj_Factory__Schemas

    def __init__(self):
        super().__init__()
        self.schema_factory = MGraph__Obj_Factory__Schemas()

    def create__Model__MGraph__Types(self):
        types = object.__new__(Model__MGraph__Types)
        types_dict = dict(node_model_type = Model__MGraph__Node,
                         edge_model_type = Model__MGraph__Edge)
        object.__setattr__(types, '__dict__', types_dict)
        return types

    def create__Model__MGraph__Node(self):
        node = object.__new__(Model__MGraph__Node)
        node_dict = dict(data = self.schema_factory.create__Schema__MGraph__Node())
        object.__setattr__(node, '__dict__', node_dict)
        return node

    def create__Model__MGraph__Edge(self):
        edge = object.__new__(Model__MGraph__Edge)
        edge_dict = dict(data = self.schema_factory.create__Schema__MGraph__Edge())
        object.__setattr__(edge, '__dict__', edge_dict)
        return edge

    def create__Model__MGraph__Graph(self):
        graph = object.__new__(Model__MGraph__Graph)
        graph_dict = dict(data       = self.schema_factory.create__Schema__MGraph__Graph(),
                          model_types = self.create__Model__MGraph__Types())
        object.__setattr__(graph, '__dict__', graph_dict)
        return graph