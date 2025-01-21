from unittest                                                       import TestCase
from osbot_utils.helpers.trace.Trace_Call                           import trace_calls
from osbot_utils.helpers.Obj_Id                                     import Obj_Id
from osbot_utils.utils.Objects                                      import __, type_full_name
from osbot_utils.testing.performance.Performance_Measure__Session   import Performance_Measure__Session
from mgraph_ai.providers.json.actions.MGraph__Json__Obj_Factory     import MGraph__Json__Obj_Factory
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data            import Schema__MGraph__Node__Data
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node    import Schema__MGraph__Json__Node


class test_MGraph__Json__Obj_Factory(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.assert_enabled = True
        cls.session        = Performance_Measure__Session(assert_enabled=cls.assert_enabled)
        cls.obj_factory    = MGraph__Json__Obj_Factory()

    def test_create__Schema__MGraph__Node__Data(self):
        schema_node_data = self.obj_factory.create__Schema__MGraph__Node__Data()
        with schema_node_data as _:
            assert type(_) is Schema__MGraph__Node__Data
            assert _.obj() == __()

    def test_create__Schema__MGraph__Json__Node(self):
        schema_json_node = self.obj_factory.create__Schema__MGraph__Json__Node()
        with schema_json_node as _:
            assert type(_)           is Schema__MGraph__Json__Node
            assert type(_.node_data) is Schema__MGraph__Node__Data
            assert type(_.node_id  ) is Obj_Id
            assert type(_.node_type) is type
            assert _.obj()           == __(node_data = __()                                      ,
                                           node_id   = _.node_id                       ,
                                           node_type = type_full_name(Schema__MGraph__Json__Node))



    def test__perf__Schema__MGraph__Json__Node(self):
        with self.session as _:
            print()
            print()
            _.measure(self.obj_factory.create__Schema__MGraph__Node__Data).print().assert_time__less_than(200)
            _.measure(self.obj_factory.create__Schema__MGraph__Json__Node).print().assert_time__less_than(1000)
            # _.measure(Schema__MGraph__Json__Node                         ).print(34)
            # _.measure(Obj_Id                                             ).print(34)


# @trace_calls( include         = ['*'],
    #               show_duration   = True ,
    #               duration_padding= 120  ,
    #               show_class      = True ,
    # )