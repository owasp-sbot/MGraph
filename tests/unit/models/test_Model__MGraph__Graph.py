import pytest
from unittest                                       import TestCase
from mgraph_ai.schemas.Schema__MGraph__Node         import Schema__MGraph__Node
from osbot_utils.utils.Objects                      import __
from osbot_utils.helpers.Random_Guid                import Random_Guid
from mgraph_ai.models.Model__MGraph__Graph          import Model__MGraph__Graph
from mgraph_ai.schemas.Schema__MGraph__Graph        import Schema__MGraph__Graph
from mgraph_ai.schemas.Schema__MGraph__Graph_Config import Schema__MGraph__Graph_Config

class test_Model__MGraph__Graph(TestCase):

    @classmethod
    def setUpClass(cls):                                                                               # Set up test data once for all tests
        cls.graph_config = Schema__MGraph__Graph_Config()
        cls.graph_schema = Schema__MGraph__Graph       (graph_config = cls.graph_config)

        cls.graph       = Model__MGraph__Graph(data=cls.graph_schema)
        cls.graph_id    = cls.graph.graph().graph_config.graph_id

    def setUp(self):
        self.node_1    = self.graph.new_node("source")
        self.node_2    = self.graph.new_node("target")
        self.node_1_id = self.node_1.node_config.node_id
        self.node_2_id = self.node_2.node_config.node_id
        self.edge_1    = self.graph.new_edge(self.node_1_id, self.node_2_id)
        self.edge_1_id = self.edge_1.edge_config.edge_id

    def tearDown(self):
        with self.graph as _:
            _.remove_edge(self.edge_1_id)
            _.remove_node(self.node_1_id)
            _.remove_node(self.node_2_id)
            assert _.data.nodes == {}
            assert _.data.edges == {}

    def test__init__(self):
        with Model__MGraph__Graph() as _:
            graph_id = _.data.graph_config.graph_id
            assert _.obj() == __(data=__(edges        = __()                            ,
                                         graph_config = __(default_edge_type = None     ,
                                                           default_node_type = None     ,
                                                           graph_id          = graph_id ,
                                                           graph_type        = None     ),
                                         nodes        = __()                            ))

    def test_new_node(self):                                                                          # Test node creation with type validation
        with self.graph.new_node(value="test_value") as _:
            node_id = _.node_config.node_id
            assert type(_)                        == Schema__MGraph__Node
            assert _                              in list(self.graph.nodes())
            assert _.obj()                        == __(attributes  = __(),
                                                        node_config = __(node_id    = node_id       ,
                                                                         node_type  = None          ,
                                                                         value_type = 'builtins.str'),
                                                        value      = "test_value"                   )

            assert _.value                         == "test_value"
            assert _.node_config.node_type         is None
            assert self.graph.remove_node(node_id) is True

    def test_new_edge(self):                                                                         # Test edge creation between nodes
        with self.graph.new_edge(self.node_1_id, self.node_2_id) as _:
            assert len(self.graph.data.edges) == 2

            invalid_id = Random_Guid()
            with pytest.raises(ValueError, match=f"Node {invalid_id} not found"):                                               # Test invalid source node
                self.graph.new_edge(invalid_id, self.node_2_id)

            self.graph.remove_edge(_.edge_config.edge_id)

    def test_remove_node(self):                                                                      # Test node removal with edge cleanup
        self.graph.remove_node(self.node_1_id)
        assert self.node_1_id                     not in self.graph.data.nodes
        assert len(self.graph.data.edges)             == 0
        assert self.graph.remove_node(self.node_2_id) is True
        assert self.graph.remove_node(self.node_2_id) is False
        assert self.graph.remove_node(Random_Guid())  is False

    def test_remove_edge(self):                                                                      # Test edge removal
        assert self.graph.remove_edge(self.edge_1_id) is True
        assert self.graph.remove_node(self.node_1_id) is True
        assert self.graph.remove_node(self.node_2_id) is True
        assert len(self.graph.data.edges) == 0
        assert self.graph.remove_edge(Random_Guid()) is False
