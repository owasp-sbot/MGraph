from unittest                                                                 import TestCase
from osbot_utils.testing.performance.Performance_Measure__Session             import Performance_Measure__Session
from osbot_utils.utils.Objects                                                import __, type_full_name
from mgraph_ai.providers.json.actions.MGraph__Json__Obj_Factory__Models       import MGraph__Json__Obj_Factory__Models
from mgraph_ai.providers.json.models.Model__MGraph__Json__Edge                import Model__MGraph__Json__Edge
from mgraph_ai.providers.json.models.Model__MGraph__Json__Graph               import Model__MGraph__Json__Graph
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node                import Model__MGraph__Json__Node
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node__Dict          import Model__MGraph__Json__Node__Dict
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node__List          import Model__MGraph__Json__Node__List
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node__Property      import Model__MGraph__Json__Node__Property
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node__Value         import Model__MGraph__Json__Node__Value
from mgraph_ai.providers.json.models.Model__MGraph__Json__Types               import Model__MGraph__Json__Types
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config                    import Schema__MGraph__Edge__Config
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Edge              import Schema__MGraph__Json__Edge
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Graph             import Schema__MGraph__Json__Graph
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__Dict        import Schema__MGraph__Json__Node__Dict
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__List        import Schema__MGraph__Json__Node__List
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__Property    import Schema__MGraph__Json__Node__Property
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__Value       import Schema__MGraph__Json__Node__Value
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Graph__Data       import Schema__MGraph__Json__Graph__Data
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node              import Schema__MGraph__Json__Node
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__Value__Data import Schema__MGraph__Json__Node__Value__Data

class test_MGraph__Json__Obj_Factory__Models(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.assert_enabled = False
        cls.session = Performance_Measure__Session(assert_enabled=cls.assert_enabled)
        cls.models_factory = MGraph__Json__Obj_Factory__Models()

    def test_create_all_objects(self):
        with self.session as _:
            print()
            print()
            _.padding = 50
            _.measure(self.models_factory.create__Model__MGraph__Json__Types          ).print().assert_time__less_than(500)
            _.measure(self.models_factory.create__Model__MGraph__Json__Node           ).print().assert_time__less_than(3000)
            _.measure(self.models_factory.create__Model__MGraph__Json__Node__Value    ).print().assert_time__less_than(3000)
            _.measure(self.models_factory.create__Model__MGraph__Json__Node__Property ).print().assert_time__less_than(3000)
            _.measure(self.models_factory.create__Model__MGraph__Json__Node__Dict     ).print().assert_time__less_than(3000)
            _.measure(self.models_factory.create__Model__MGraph__Json__Node__List     ).print().assert_time__less_than(3000)
            _.measure(self.models_factory.create__Model__MGraph__Json__Edge           ).print().assert_time__less_than(4000)
            _.measure(self.models_factory.create__Model__MGraph__Json__Graph          ).print().assert_time__less_than(5000)
            print()
            _.measure(Model__MGraph__Json__Types          ).print()
            _.measure(Model__MGraph__Json__Node__Value    ).print()
            _.measure(Model__MGraph__Json__Node__Property ).print()
            _.measure(Model__MGraph__Json__Node__Dict     ).print()
            _.measure(Model__MGraph__Json__Node__List     ).print()
            _.measure(Model__MGraph__Json__Edge           ).print()
            _.measure(Model__MGraph__Json__Graph          ).print()

    def test_create__Model__MGraph__Json__Types(self):
        types = self.models_factory.create__Model__MGraph__Json__Types()
        with types as _:
            assert type(_)               is Model__MGraph__Json__Types
            assert _.node_model_type     is Model__MGraph__Json__Node
            assert _.edge_model_type     is Model__MGraph__Json__Edge
            assert _.obj()               == __(node_model_type = type_full_name(Model__MGraph__Json__Node),
                                             edge_model_type = type_full_name(Model__MGraph__Json__Edge))

    def test_create__Model__MGraph__Json__Node(self):
        node = self.models_factory.create__Model__MGraph__Json__Node()
        with node as _:
            assert type(_)           is Model__MGraph__Json__Node
            assert type(_.data)      is Schema__MGraph__Json__Node
            assert _.obj()           == __(data = __(node_data = __(),
                                                     node_id   = _.data.node_id,
                                                     node_type = type_full_name(Schema__MGraph__Json__Node)))

    def test_create__Model__MGraph__Json__Node__Value(self):
        node = self.models_factory.create__Model__MGraph__Json__Node__Value()
        with node as _:
            assert type(_)           is Model__MGraph__Json__Node__Value
            assert type(_.data)      is Schema__MGraph__Json__Node__Value
            assert type(_.data.node_data) is Schema__MGraph__Json__Node__Value__Data
            assert _.obj()           == __(data = __(node_data = __(value = None,
                                                                  value_type = type_full_name(str)),
                                                   node_id = _.data.node_id,
                                                   node_type = type_full_name(Schema__MGraph__Json__Node__Value)))

    def test_create__Model__MGraph__Json__Node__Property(self):
        node = self.models_factory.create__Model__MGraph__Json__Node__Property()
        with node as _:
            assert type(_)           is Model__MGraph__Json__Node__Property
            assert type(_.data)      is Schema__MGraph__Json__Node__Property
            assert _.obj()           == __(data = __(node_data = __(name = ''),
                                                   node_id = _.data.node_id,
                                                   node_type = type_full_name(Schema__MGraph__Json__Node__Property)))

    def test_create__Model__MGraph__Json__Node__Dict(self):
        node = self.models_factory.create__Model__MGraph__Json__Node__Dict()
        with node as _:
            assert type(_)           is Model__MGraph__Json__Node__Dict
            assert type(_.data)      is Schema__MGraph__Json__Node__Dict
            assert _.obj()           == __(data = __(node_data = __(),
                                                   node_id = _.data.node_id,
                                                   node_type = type_full_name(Schema__MGraph__Json__Node__Dict)))

    def test_create__Model__MGraph__Json__Node__List(self):
        node = self.models_factory.create__Model__MGraph__Json__Node__List()
        with node as _:
            assert type(_)           is Model__MGraph__Json__Node__List
            assert type(_.data)      is Schema__MGraph__Json__Node__List
            assert _.obj()           == __(data = __(node_data = __(),
                                                   node_id = _.data.node_id,
                                                   node_type = type_full_name(Schema__MGraph__Json__Node__List)))

    def test_create__Model__MGraph__Json__Edge(self):
        edge = self.models_factory.create__Model__MGraph__Json__Edge()
        with edge as _:
            assert type(_)           is Model__MGraph__Json__Edge
            assert type(_.data)      is Schema__MGraph__Json__Edge
            assert _.obj()           == __(data = __(edge_config = __(edge_id = _.data.edge_config.edge_id),
                                                   edge_data = __(),
                                                   edge_type = type_full_name(Schema__MGraph__Json__Edge),
                                                   from_node_id = _.data.from_node_id,
                                                   to_node_id = _.data.to_node_id))

    def test_create__Model__MGraph__Json__Graph(self):
        graph = self.models_factory.create__Model__MGraph__Json__Graph()
        with graph as _:
            assert type(_)              is Model__MGraph__Json__Graph
            assert type(_.data)         is Schema__MGraph__Json__Graph
            assert type(_.model_types)  is Model__MGraph__Json__Types
            assert _.obj()              == __(data = __(edges = __(),
                                                      graph_data = __(root_id = None),
                                                      graph_id = _.data.graph_id,
                                                      graph_type = type_full_name(Schema__MGraph__Json__Graph),
                                                      nodes = __(),
                                                      schema_types = __(edge_type = type_full_name(Schema__MGraph__Json__Edge),
                                                                      edge_config_type = type_full_name(Schema__MGraph__Edge__Config),
                                                                      graph_data_type = type_full_name(Schema__MGraph__Json__Graph__Data),
                                                                      node_type = type_full_name(Schema__MGraph__Json__Node),
                                                                      node_data_type = type_full_name(Schema__MGraph__Json__Node__Value__Data))),
                                            model_types = __(node_model_type = type_full_name(Model__MGraph__Json__Node),
                                                           edge_model_type = type_full_name(Model__MGraph__Json__Edge)))