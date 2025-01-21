from osbot_utils.helpers.Obj_Id                             import Obj_Id
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge          import Schema__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config  import Schema__MGraph__Edge__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Data    import Schema__MGraph__Edge__Data
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph         import Schema__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph__Data   import Schema__MGraph__Graph__Data
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node          import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data    import Schema__MGraph__Node__Data
from mgraph_ai.mgraph.schemas.Schema__MGraph__Types         import Schema__MGraph__Types
from osbot_utils.type_safe.Type_Safe                        import Type_Safe

class MGraph__Obj_Factory__Schemas(Type_Safe):

    def create__Schema__MGraph__Node__Data(self):
        node_data = object.__new__(Schema__MGraph__Node__Data)
        object.__setattr__(node_data, '__dict__', {})
        return node_data

    def create__Schema__MGraph__Node(self):
        node_data = self.create__Schema__MGraph__Node__Data()
        node      = object.__new__(Schema__MGraph__Node)
        node_dict = dict(node_data = node_data           ,
                         node_id   = Obj_Id()            ,
                         node_type = Schema__MGraph__Node)
        object.__setattr__(node, '__dict__', node_dict)
        return node

    def create__Schema__MGraph__Edge__Data(self):
        edge_data = object.__new__(Schema__MGraph__Edge__Data)
        object.__setattr__(edge_data, '__dict__', {})
        return edge_data

    def create__Schema__MGraph__Edge__Config(self):
        edge_config      = object.__new__(Schema__MGraph__Edge__Config)
        edge_config_dict = dict(edge_id = Obj_Id())
        object.__setattr__(edge_config, '__dict__', edge_config_dict)
        return edge_config

    def create__Schema__MGraph__Edge(self):
        edge      = object.__new__(Schema__MGraph__Edge)
        edge_dict = dict(edge_config    = self.create__Schema__MGraph__Edge__Config(),
                         edge_data      = self.create__Schema__MGraph__Edge__Data  (),
                         edge_type      = Schema__MGraph__Edge                       ,
                         from_node_id   = Obj_Id()                                   ,
                         to_node_id     = Obj_Id()                                   )
        object.__setattr__(edge, '__dict__', edge_dict)
        return edge

    def create__Schema__MGraph__Graph__Data(self):
        graph_data = object.__new__(Schema__MGraph__Graph__Data)
        object.__setattr__(graph_data, '__dict__', {})
        return graph_data

    def create__Schema__MGraph__Types(self):
        types      = object.__new__(Schema__MGraph__Types)
        types_dict = dict(edge_type        = Schema__MGraph__Edge        ,
                          edge_config_type = Schema__MGraph__Edge__Config,
                          graph_data_type  = Schema__MGraph__Graph__Data ,
                          node_type        = Schema__MGraph__Node        ,
                          node_data_type   = Schema__MGraph__Node__Data  )
        object.__setattr__(types, '__dict__', types_dict)
        return types

    def create__Schema__MGraph__Graph(self):
        graph      = object.__new__(Schema__MGraph__Graph)
        graph_dict = dict(edges        = {}                                        ,
                          graph_data   = self.create__Schema__MGraph__Graph__Data(),
                          graph_id     = Obj_Id()                                  ,
                          graph_type   = Schema__MGraph__Graph                     ,
                          nodes        = {}                                        ,
                          schema_types = self.create__Schema__MGraph__Types      ())
        object.__setattr__(graph, '__dict__', graph_dict)
        return graph