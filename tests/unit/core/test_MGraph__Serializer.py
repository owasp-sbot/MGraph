from unittest                           import TestCase
from osbot_utils.utils.Files            import current_temp_folder, file_create
from osbot_utils.helpers.Local_Cache    import Local_Cache
from osbot_utils.utils.Misc             import list_set
from osbot_utils.helpers.Random_Seed    import Random_Seed
from mgraph_ai.core.MGraph              import MGraph
from mgraph_ai.core.MGraph__Serializer  import MGraph__Serializer, Serialization_Mode
from mgraph_ai.core.MGraphs             import MGraphs

class test_MGraph__Serializer(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.graph_key = __name__
        with Random_Seed(enabled=False):
            cls.mgraph       = MGraphs().new__random(graph_key=cls.graph_key)              # todo: see if we need to make this non-random
        cls.graph_serializer = MGraph__Serializer(mgraph = cls.mgraph)

    @classmethod
    def tearDownClass(cls):
        (cls
         .graph_serializer.local_cache.cache_delete())


    def test__init__(self):
        expected_attrs = ['caches_name', 'key', 'local_cache', 'mgraph', 'mode']
        with self.graph_serializer as _:
            assert _.__attr_names__() == expected_attrs
            assert _.caches_name     == 'mgraph_tests'
            assert _.mgraph.__class__ is MGraph
            assert _.mode             == Serialization_Mode.PICKLE
            assert _.key              == f'serialiser_for__{self.mgraph.key}'

            assert _.__annotations__.get('local_cache') is Local_Cache
            assert type(_.local_cache) is Local_Cache
            assert _.local_cache.info() == { 'cache_name'     : _.key                           ,
                                             'caches_name'    : _.caches_name                   ,
                                             'data_keys'      : list_set(_.local_cache.data())  ,
                                             'path_cache_file': f'{current_temp_folder()}/{_.caches_name}/{_.key}.json'}





    def test_save(self):
        with self.graph_serializer as _:
            assert _.save() == '...pickle save - to be implemented...'              # todo: implement this test
            _.mode = Serialization_Mode.JSON
            assert _.save() == True


    def test_save_to_json(self):
        with self.graph_serializer as _:
            assert _.save_to_json() is True
            assert _.mgraph.data().graph_data() == _.local_cache.get('graph_data')
            #_.mgraph.print()

    def test_save_to_pickle(self):
        with self.graph_serializer as _:
            assert _.save_to_pickle() == '...pickle save - to be implemented...'

#     def test_mermaid(self):
#         file_name = 'test_mermaid.md'
#         code = """
# ```mermaid
# graph LR;
#     subgraph BBBB
#         Z("some text")
#         Y[["aaaaa"]]
#     end
#     subgraph AAAAA
#         Z --> Y
#         A --> B
#         subgraph CCCC
#             A ---> C
#             A ----> D
#             subgraph DDDDD
#                 A -----> E
#                 A ----> F
#             end
#             F -----> C
#         end
#     end
#
#     C ---> Z
# ```"""
#         file_create(file_name, code)