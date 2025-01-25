from unittest                                                      import TestCase
from osbot_utils.utils.Objects                                     import __, type_full_name
from osbot_utils.testing.performance.Performance_Measure__Session  import Performance_Measure__Session
from mgraph_ai.mgraph.actions.MGraph__Obj_Factory__Schemas         import MGraph__Obj_Factory__Schemas
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge                 import Schema__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config         import Schema__MGraph__Edge__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Data           import Schema__MGraph__Edge__Data
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph                import Schema__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph__Data          import Schema__MGraph__Graph__Data
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node                 import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data           import Schema__MGraph__Node__Data
from mgraph_ai.mgraph.schemas.Schema__MGraph__Types                import Schema__MGraph__Types
from osbot_utils.helpers.Obj_Id                                    import Obj_Id


class test_MGraph__Obj_Factory__Schemas(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.assert_enabled = False
        cls.session        = Performance_Measure__Session(assert_enabled=cls.assert_enabled)
        cls.obj_factory    = MGraph__Obj_Factory__Schemas()

    def test_create_all_objects(self):
        with self.session as _:
            print()
            print()
            _.padding = 36
            _.measure(self.obj_factory.create__Schema__MGraph__Node__Data  ).print().assert_time__less_than(300 )
            _.measure(self.obj_factory.create__Schema__MGraph__Node        ).print().assert_time__less_than(1000)
            _.measure(self.obj_factory.create__Schema__MGraph__Edge__Data  ).print().assert_time__less_than(300 )
            _.measure(self.obj_factory.create__Schema__MGraph__Edge__Config).print().assert_time__less_than(1000)
            _.measure(self.obj_factory.create__Schema__MGraph__Edge        ).print().assert_time__less_than(2000)
            _.measure(self.obj_factory.create__Schema__MGraph__Graph__Data ).print().assert_time__less_than(200 )
            _.measure(self.obj_factory.create__Schema__MGraph__Types       ).print().assert_time__less_than(500 )
            _.measure(self.obj_factory.create__Schema__MGraph__Graph       ).print().assert_time__less_than(1000)
            print()
            _.measure(Schema__MGraph__Node__Data  ).print()
            _.measure(Schema__MGraph__Node        ).print()
            _.measure(Schema__MGraph__Edge__Data  ).print()
            _.measure(Schema__MGraph__Edge__Config).print()
            _.measure(Schema__MGraph__Edge        ).print()
            _.measure(Schema__MGraph__Graph__Data ).print()
            _.measure(Schema__MGraph__Types       ).print()
            _.measure(Schema__MGraph__Graph       ).print()


    def test_create__Schema__MGraph__Node__Data(self):
        node_data = self.obj_factory.create__Schema__MGraph__Node__Data()
        with node_data as _:
            assert type(_)    is Schema__MGraph__Node__Data
            assert _.obj()    == __()

    def test_create__Schema__MGraph__Node(self):
        node = self.obj_factory.create__Schema__MGraph__Node()
        with node as _:
            assert type(_)           is Schema__MGraph__Node
            assert type(_.node_data) is Schema__MGraph__Node__Data
            assert type(_.node_id)   is Obj_Id
            assert type(_.node_type) is type
            assert _.obj()           == __(node_data = __()                                ,
                                          node_id   = _.node_id                            ,
                                          node_type = type_full_name(Schema__MGraph__Node))

    def test_create__Schema__MGraph__Edge__Data(self):
        edge_data = self.obj_factory.create__Schema__MGraph__Edge__Data()
        with edge_data as _:
            assert type(_)    is Schema__MGraph__Edge__Data
            assert _.obj()    == __()

    def test_create__Schema__MGraph__Edge__Config(self):
        edge_config = self.obj_factory.create__Schema__MGraph__Edge__Config()
        with edge_config as _:
            assert type(_)         is Schema__MGraph__Edge__Config
            assert type(_.edge_id) is Obj_Id
            assert _.obj()         == __(edge_id = _.edge_id)

    def test_create__Schema__MGraph__Edge(self):
        edge = self.obj_factory.create__Schema__MGraph__Edge()
        with edge as _:
            assert type(_)              is Schema__MGraph__Edge
            assert type(_.edge_config)  is Schema__MGraph__Edge__Config
            assert type(_.edge_data)    is Schema__MGraph__Edge__Data
            assert type(_.edge_type)    is type
            assert type(_.from_node_id) is Obj_Id
            assert type(_.to_node_id)   is Obj_Id
            assert _.obj()              == __(edge_config  = __(edge_id = _.edge_config.edge_id),
                                             edge_data    = __()                                ,
                                             edge_type    = type_full_name(Schema__MGraph__Edge),
                                             from_node_id = _.from_node_id                      ,
                                             to_node_id   = _.to_node_id                        )

    def test_create__Schema__MGraph__Graph__Data(self):
        graph_data = self.obj_factory.create__Schema__MGraph__Graph__Data()
        with graph_data as _:
            assert type(_)    is Schema__MGraph__Graph__Data
            assert _.obj()    == __()

    def test_create__Schema__MGraph__Types(self):
        types = self.obj_factory.create__Schema__MGraph__Types()
        with types as _:
            assert type(_)                 is Schema__MGraph__Types
            assert _.edge_type             is Schema__MGraph__Edge
            assert _.edge_config_type      is Schema__MGraph__Edge__Config
            assert _.graph_data_type       is Schema__MGraph__Graph__Data
            assert _.node_type             is Schema__MGraph__Node
            assert _.node_data_type        is Schema__MGraph__Node__Data
            assert _.obj()                 == __(edge_type        = type_full_name(Schema__MGraph__Edge)      ,
                                               edge_config_type = type_full_name(Schema__MGraph__Edge__Config),
                                               graph_data_type  = type_full_name(Schema__MGraph__Graph__Data) ,
                                               node_type        = type_full_name(Schema__MGraph__Node)        ,
                                               node_data_type   = type_full_name(Schema__MGraph__Node__Data)  )

    def test_create__Schema__MGraph__Graph(self):
        graph = self.obj_factory.create__Schema__MGraph__Graph()
        with graph as _:
            assert type(_)              is Schema__MGraph__Graph
            assert type(_.edges)        is dict
            assert type(_.graph_data)   is Schema__MGraph__Graph__Data
            assert type(_.graph_id)     is Obj_Id
            assert type(_.graph_type)   is type
            assert type(_.nodes)        is dict
            assert type(_.schema_types) is Schema__MGraph__Types
            assert _.obj()              == __(edges       = __()                                    ,
                                             graph_data   = __()                                    ,
                                             graph_id     = _.graph_id                              ,
                                             graph_type   = type_full_name(Schema__MGraph__Graph)   ,
                                             nodes        = __()                                    ,
                                             schema_types = __(edge_type        = type_full_name(Schema__MGraph__Edge)      ,
                                                             edge_config_type = type_full_name(Schema__MGraph__Edge__Config),
                                                             graph_data_type  = type_full_name(Schema__MGraph__Graph__Data) ,
                                                             node_type        = type_full_name(Schema__MGraph__Node)        ,
                                                             node_data_type   = type_full_name(Schema__MGraph__Node__Data)  ))