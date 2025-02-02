from unittest                                                                    import TestCase
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                               import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data                         import Schema__MGraph__Node__Data
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node                 import Schema__MGraph__Json__Node
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Property__Data import Schema__MGraph__Json__Node__Property__Data
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value__Data    import Schema__MGraph__Json__Node__Value__Data
from osbot_utils.testing.performance.Performance_Measure__Session                import Performance_Measure__Session
from osbot_utils.type_safe.Type_Safe                                             import Type_Safe
from osbot_utils.utils.Objects                                                   import __, type_full_name, base_types
from mgraph_db.providers.json.actions.MGraph__Json__Obj_Factory__Schemas         import MGraph__Json__Obj_Factory__Schemas
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Edge                 import Schema__MGraph__Json__Edge
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Graph                import Schema__MGraph__Json__Graph
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Graph__Data          import Schema__MGraph__Json__Graph__Data
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Dict           import Schema__MGraph__Json__Node__Dict
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__List           import Schema__MGraph__Json__Node__List
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Property       import Schema__MGraph__Json__Node__Property
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value          import Schema__MGraph__Json__Node__Value
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Types                import Schema__MGraph__Json__Types
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge__Config                       import Schema__MGraph__Edge__Config

class test_MGraph__Json__Obj_Factory__Schemas(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.assert_enabled = False
        cls.session = Performance_Measure__Session(assert_enabled=cls.assert_enabled)
        cls.json_factory = MGraph__Json__Obj_Factory__Schemas()

    def test_create_all_objects(self):
        with self.session as _:
            print()
            print()
            _.padding = 50
            _.measure(self.json_factory.create__Schema__MGraph__Json__Node                ).print().assert_time__less_than(300)
            _.measure(Schema__MGraph__Json__Node                                          ).print().assert_time__less_than(300)
            print()
            _.measure(self.json_factory.create__Schema__MGraph__Json__Node__Value__Data   ).print().assert_time__less_than(300)
            _.measure(Schema__MGraph__Json__Node__Value__Data                             ).print().assert_time__less_than(300)
            print()
            _.measure(self.json_factory.create__Schema__MGraph__Json__Node__Property__Data).print().assert_time__less_than(300)
            _.measure(Schema__MGraph__Json__Node__Property__Data                          ).print().assert_time__less_than(300)
            print()
            _.measure(self.json_factory.create__Schema__MGraph__Json__Node__Value         ).print().assert_time__less_than(1000)
            _.measure(Schema__MGraph__Json__Node__Value                                   ).print().assert_time__less_than(300)
            print()
            _.measure(self.json_factory.create__Schema__MGraph__Json__Node__Property      ).print().assert_time__less_than(1000)
            _.measure(Schema__MGraph__Json__Node__Property                                ).print().assert_time__less_than(300)
            print()
            _.measure(self.json_factory.create__Schema__MGraph__Json__Node__Dict          ).print().assert_time__less_than(1000)
            _.measure(self.json_factory.create__Schema__MGraph__Json__Node__List          ).print().assert_time__less_than(1000)
            _.measure(self.json_factory.create__Schema__MGraph__Json__Edge                ).print().assert_time__less_than(2000)
            _.measure(Schema__MGraph__Json__Edge                                          ).print().assert_time__less_than(300)
            print()
            _.measure(self.json_factory.create__Schema__MGraph__Json__Graph__Data         ).print().assert_time__less_than(300)
            _.measure(Schema__MGraph__Json__Graph__Data                                   ).print().assert_time__less_than(300)
            print()
            _.measure(self.json_factory.create__Schema__MGraph__Json__Types               ).print().assert_time__less_than(500)
            _.measure(Schema__MGraph__Json__Types                                         ).print().assert_time__less_than(500)
            print()
            _.measure(self.json_factory.create__Schema__MGraph__Json__Graph               ).print().assert_time__less_than(3000)
            _.measure(Schema__MGraph__Json__Graph                                         ).print().assert_time__less_than(500)

    def test_create__Schema__MGraph__Json__Node(self):
        node = self.json_factory.create__Schema__MGraph__Json__Node()
        with node as _:
            assert type(_)           is Schema__MGraph__Json__Node
            assert type(_.node_data) is Schema__MGraph__Node__Data
            assert base_types(_)     == [Schema__MGraph__Node, Type_Safe, object]
            assert _.obj()           == __(node_data = __(),
                                           node_id   = _.node_id,
                                           node_type = type_full_name(Schema__MGraph__Json__Node))

    def test_create__Schema__MGraph__Json__Node__Value__Data(self):
        data = self.json_factory.create__Schema__MGraph__Json__Node__Value__Data()
        with data as _:
            assert type(_)          is Schema__MGraph__Json__Node__Value__Data
            assert type(_.value)    is type(None)
            assert _.value_type     is str
            assert _.obj()          == __(value = None, value_type = type_full_name(str))

    def test_create__Schema__MGraph__Json__Node__Property__Data(self):
        data = self.json_factory.create__Schema__MGraph__Json__Node__Property__Data()
        with data as _:
            assert type(_)     is Schema__MGraph__Json__Node__Property__Data
            assert _.name     == ''
            assert _.obj()     == __(name = '')

    def test_create__Schema__MGraph__Json__Node__Value(self):
        node = self.json_factory.create__Schema__MGraph__Json__Node__Value()
        with node as _:
            assert type(_)           is Schema__MGraph__Json__Node__Value
            assert type(_.node_data) is Schema__MGraph__Json__Node__Value__Data
            assert _.obj()           == __(node_data = __(value = None, value_type = type_full_name(str)),
                                         node_id = _.node_id,
                                         node_type = type_full_name(Schema__MGraph__Json__Node__Value))

    def test_create__Schema__MGraph__Json__Node__Property(self):
        node = self.json_factory.create__Schema__MGraph__Json__Node__Property()
        with node as _:
            assert type(_)           is Schema__MGraph__Json__Node__Property
            assert type(_.node_data) is Schema__MGraph__Json__Node__Property__Data
            assert _.obj()           == __(node_data = __(name = ''),
                                         node_id = _.node_id,
                                         node_type = type_full_name(Schema__MGraph__Json__Node__Property))

    def test_create__Schema__MGraph__Json__Node__Dict(self):
        node = self.json_factory.create__Schema__MGraph__Json__Node__Dict()
        with node as _:
            assert type(_) is Schema__MGraph__Json__Node__Dict
            assert _.obj() == __(node_data = __(),
                               node_id = _.node_id,
                               node_type = type_full_name(Schema__MGraph__Json__Node__Dict))

    def test_create__Schema__MGraph__Json__Node__List(self):
        node = self.json_factory.create__Schema__MGraph__Json__Node__List()
        with node as _:
            assert type(_) is Schema__MGraph__Json__Node__List
            assert _.obj() == __(node_data = __(),
                               node_id = _.node_id,
                               node_type = type_full_name(Schema__MGraph__Json__Node__List))

    def test_create__Schema__MGraph__Json__Edge(self):
        edge = self.json_factory.create__Schema__MGraph__Json__Edge()
        with edge as _:
            assert type(_)              is Schema__MGraph__Json__Edge
            assert type(_.edge_config)  is Schema__MGraph__Edge__Config
            assert _.obj()              == __(edge_config  = __(edge_id = _.edge_config.edge_id),
                                            edge_data    = __(),
                                            edge_type    = type_full_name(Schema__MGraph__Json__Edge),
                                            from_node_id = _.from_node_id,
                                            to_node_id   = _.to_node_id)

    def test_create__Schema__MGraph__Json__Graph__Data(self):
        data = self.json_factory.create__Schema__MGraph__Json__Graph__Data()
        with data as _:
            assert type(_)      is Schema__MGraph__Json__Graph__Data
            assert _.root_id   is None
            assert _.obj()      == __(root_id = None)

    def test_create__Schema__MGraph__Json__Types(self):
        types = self.json_factory.create__Schema__MGraph__Json__Types()
        with types as _:
            assert type(_)                is Schema__MGraph__Json__Types
            assert _.edge_type            is Schema__MGraph__Json__Edge
            assert _.edge_config_type     is Schema__MGraph__Edge__Config
            assert _.graph_data_type      is Schema__MGraph__Json__Graph__Data
            assert _.node_type            is Schema__MGraph__Json__Node
            assert _.node_data_type       is Schema__MGraph__Json__Node__Value__Data
            assert _.obj()                == __(edge_type        = type_full_name(Schema__MGraph__Json__Edge),
                                              edge_config_type = type_full_name(Schema__MGraph__Edge__Config),
                                              graph_data_type  = type_full_name(Schema__MGraph__Json__Graph__Data),
                                              node_type        = type_full_name(Schema__MGraph__Json__Node),
                                              node_data_type   = type_full_name(Schema__MGraph__Json__Node__Value__Data))

    def test_create__Schema__MGraph__Json__Graph(self):
        graph = self.json_factory.create__Schema__MGraph__Json__Graph()
        with graph as _:
            assert type(_)              is Schema__MGraph__Json__Graph
            assert type(_.graph_data)   is Schema__MGraph__Json__Graph__Data
            assert type(_.schema_types) is Schema__MGraph__Json__Types
            assert _.obj()              == __(edges        = __(),
                                            graph_data   = __(root_id = None),
                                            graph_id     = _.graph_id,
                                            graph_type   = type_full_name(Schema__MGraph__Json__Graph),
                                            nodes        = __(),
                                            schema_types = __(edge_type        = type_full_name(Schema__MGraph__Json__Edge),
                                                            edge_config_type = type_full_name(Schema__MGraph__Edge__Config),
                                                            graph_data_type  = type_full_name(Schema__MGraph__Json__Graph__Data),
                                                            node_type        = type_full_name(Schema__MGraph__Json__Node),
                                                            node_data_type   = type_full_name(Schema__MGraph__Json__Node__Value__Data)))