from unittest                                                           import TestCase
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node        import Schema__MGraph__Json__Node__Dict
from osbot_utils.utils.Objects                                          import __, type_full_name
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node         import Domain__MGraph__Json__Node
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node__Dict   import Domain__MGraph__Json__Node__Dict


class test_Domain__MGraph__Json__Node__Dict(TestCase):

    @classmethod
    def setUpClass(cls):                                                                    # Initialize test data
        cls.domain_graph     = Domain__MGraph__Json__Node()
        cls.domain_node_dict = Domain__MGraph__Json__Node__Dict(graph=cls.domain_graph.graph)
        cls.domain_graph.add_node(cls.domain_node_dict.node)

    def test__init__(self):                                                                 # Test basic initialization
        with self.domain_node_dict as _:
            assert type(_)                                   is Domain__MGraph__Json__Node__Dict
            assert isinstance(_, Domain__MGraph__Json__Node) is True
            assert _.obj() == __(node  = __(data=__(node_data  = __()                                             ,
                                                    node_id    = _.node_id                                        ,
                                                    node_type  = type_full_name(Schema__MGraph__Json__Node__Dict))),
                                 graph = _.graph.obj())

    def test_add_property(self):                                                           # Test adding properties

        with self.domain_node_dict as _:
            assert len(_.graph.nodes_ids()) == 1
            assert len(_.graph.edges_ids()) == 0

            assert _.properties() == {}
            _.add_property("test_key", "test_value")                                        # add 1st property
            assert _.properties()               == {'test_key'   : 'test_value' }
            _.add_property("another_key", 42)                                               # add 2nd property
            assert _.properties()               == {'another_key': 42           ,
                                                    'test_key'   : 'test_value' }

            assert len(_.graph.nodes_ids()) == 5
            assert len(_.graph.edges_ids()) == 4

            _.add_property("test_key", 'changed')                                           # edit 1st property

            assert _.properties()               == {'another_key': 42        ,
                                                    'test_key'   : 'changed' }

            assert len(_.graph.nodes_ids()) == 5                                            # check that these didn't change
            assert len(_.graph.edges_ids()) == 4

            _.delete_property("test_key")                                                   # delete 1st property
            assert _.properties() == {'another_key': 42 }

            _.delete_property("another_key")                                               # delete 2nd property
            assert _.properties() == {}


            assert len(_.graph.nodes_ids()) == 3                                            # BUG : this should be 1 (the property values are not being deleted)
            assert len(_.graph.edges_ids()) == 0

            assert self.domain_node_dict.node_id in _.graph.nodes_ids()                     # confirm parent node is still there



    def test_delete_property(self):
        with self.domain_node_dict as _:# Test property access
            _.add_property("key1", "value1")
            _.add_property("key2", "value2")

            assert _.property("key1"        ) == "value1"
            assert _.property("key2"        ) == "value2"
            assert _.property("non_existent") is None
            assert _.delete_property("key1" ) is True
            assert _.delete_property("key1" ) is False
            assert _.delete_property("key2" ) is True
            assert _.delete_property("key2" ) is False
            assert _.delete_property("aaaaa") is False
            assert _.properties() == {}


    def test_update(self):                                                           # Test bulk property updates
        with self.domain_node_dict as _:
            test_props = { "key1": "value1" ,
                            "key2": 42      ,
                            "key3": True    }
            _.update(test_props)

            assert _.properties() == test_props