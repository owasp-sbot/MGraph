from unittest                                                       import TestCase
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config          import Schema__MGraph__Edge__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph__Data           import Schema__MGraph__Graph__Data
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data            import Schema__MGraph__Node__Data
from osbot_utils.testing.performance.Performance_Measure__Session   import Performance_Measure__Session
from osbot_utils.utils.Objects                                      import __, type_full_name
from mgraph_ai.mgraph.actions.MGraph__Obj_Factory__Models           import MGraph__Obj_Factory__Models
from mgraph_ai.mgraph.models.Model__MGraph__Edge                    import Model__MGraph__Edge
from mgraph_ai.mgraph.models.Model__MGraph__Graph                   import Model__MGraph__Graph
from mgraph_ai.mgraph.models.Model__MGraph__Node                    import Model__MGraph__Node
from mgraph_ai.mgraph.models.Model__MGraph__Types                   import Model__MGraph__Types
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph                 import Schema__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node

class test_MGraph__Obj_Factory__Models(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.assert_enabled  = False
        cls.session         = Performance_Measure__Session(assert_enabled=cls.assert_enabled)
        cls.models_factory  = MGraph__Obj_Factory__Models()

    def test_create_all_objects(self):
        with self.session as _:
            print()
            print()
            _.padding = 36
            _.measure(self.models_factory.create__Model__MGraph__Types).print().assert_time__less_than(500)
            _.measure(self.models_factory.create__Model__MGraph__Node ).print().assert_time__less_than(2000)
            _.measure(self.models_factory.create__Model__MGraph__Edge ).print().assert_time__less_than(3000)
            _.measure(self.models_factory.create__Model__MGraph__Graph).print().assert_time__less_than(4000)
            print()
            _.measure(Model__MGraph__Types).print()
            _.measure(Model__MGraph__Node ).print()
            _.measure(Model__MGraph__Edge ).print()
            _.measure(Model__MGraph__Graph).print()

    def test_create__Model__MGraph__Types(self):
        types = self.models_factory.create__Model__MGraph__Types()
        with types as _:
            assert type(_)               is Model__MGraph__Types
            assert _.node_model_type     is Model__MGraph__Node
            assert _.edge_model_type     is Model__MGraph__Edge
            assert _.obj()               == __(node_model_type = type_full_name(Model__MGraph__Node),
                                             edge_model_type = type_full_name(Model__MGraph__Edge))

    def test_create__Model__MGraph__Node(self):
        node = self.models_factory.create__Model__MGraph__Node()
        with node as _:
            assert type(_)        is Model__MGraph__Node
            assert type(_.data)   is Schema__MGraph__Node
            assert _.obj()        == __(data = __(node_data = __(),
                                                node_id   = _.data.node_id,
                                                node_type = type_full_name(Schema__MGraph__Node)))

    def test_create__Model__MGraph__Edge(self):
        edge = self.models_factory.create__Model__MGraph__Edge()
        with edge as _:
            assert type(_)        is Model__MGraph__Edge
            assert type(_.data)   is Schema__MGraph__Edge
            assert _.obj()        == __(data = __(edge_config  = __(edge_id = _.data.edge_config.edge_id),
                                                edge_data    = __(),
                                                edge_type    = type_full_name(Schema__MGraph__Edge),
                                                from_node_id = _.data.from_node_id,
                                                to_node_id   = _.data.to_node_id))

    def test_create__Model__MGraph__Graph(self):
        graph = self.models_factory.create__Model__MGraph__Graph()
        with graph as _:
            assert type(_)               is Model__MGraph__Graph
            assert type(_.data)          is Schema__MGraph__Graph
            assert type(_.model_types)   is Model__MGraph__Types
            assert _.obj()               == __(data = __(edges        = __(),
                                                       graph_data   = __(),
                                                       graph_id     = _.data.graph_id,
                                                       graph_type   = type_full_name(Schema__MGraph__Graph),
                                                       nodes        = __(),
                                                       schema_types = __(edge_type        = type_full_name(Schema__MGraph__Edge),
                                                                       edge_config_type = type_full_name(Schema__MGraph__Edge__Config),
                                                                       graph_data_type  = type_full_name(Schema__MGraph__Graph__Data),
                                                                       node_type        = type_full_name(Schema__MGraph__Node),
                                                                       node_data_type   = type_full_name(Schema__MGraph__Node__Data))),
                                             model_types = __(node_model_type = type_full_name(Model__MGraph__Node),
                                                            edge_model_type = type_full_name(Model__MGraph__Edge)))