from unittest                                       import TestCase
from mgraph_ai.schemas.Schema__MGraph__Graph        import Schema__MGraph__Graph
from mgraph_ai.schemas.Schema__MGraph__Graph_Config import Schema__MGraph__Graph_Config
from mgraph_ai.schemas.Schema__MGraph__Node         import Schema__MGraph__Node
from mgraph_ai.schemas.Schema__MGraph__Node_Config  import Schema__MGraph__Node_Config
from mgraph_ai.schemas.Schema__MGraph__Edge         import Schema__MGraph__Edge
from mgraph_ai.schemas.Schema__MGraph__Edge_Config  import Schema__MGraph__Edge_Config
from osbot_utils.helpers.Random_Guid                import Random_Guid

class test_Schema__MGraph__Graph(TestCase):

    @classmethod
    def setUpClass(cls):
        # Create graph config
        cls.graph_config = Schema__MGraph__Graph_Config(
            graph_id          = Random_Guid(),
            graph_type       = dict,
            default_node_type = str,
            default_edge_type = bool)

        # Create a sample node
        cls.node_config = Schema__MGraph__Node_Config(
            node_id    = Random_Guid(),
            node_type  = str,
            value_type = str)
        cls.node = Schema__MGraph__Node(
            attributes  = {},
            node_config = cls.node_config,
            value      = "test_value")

        # Create a sample edge
        cls.edge_config = Schema__MGraph__Edge_Config(
            edge_id        = Random_Guid(),
            from_node_type = str,
            to_node_type   = str)
        cls.edge = Schema__MGraph__Edge(
            attributes   = {},
            edge_config  = cls.edge_config,
            from_node_id = Random_Guid(),
            to_node_id   = Random_Guid())

    def setUp(self):
        self.graph = Schema__MGraph__Graph(
            nodes        = {self.node.node_config.node_id: self.node},
            edges        = {self.edge.edge_config.edge_id: self.edge},
            graph_config = self.graph_config)

    def test__init__(self):
        assert type(self.graph) is Schema__MGraph__Graph
        assert self.graph.graph_config == self.graph_config
        assert len(self.graph.nodes) == 1
        assert len(self.graph.edges) == 1
        assert self.graph.nodes[self.node.node_config.node_id] == self.node
        assert self.graph.edges[self.edge.edge_config.edge_id] == self.edge

    def test_type_safety(self):
        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Graph(
                nodes        = "not-a-dict",         # Should be Dict
                edges        = {self.edge.edge_config.edge_id: self.edge},
                graph_config = self.graph_config)

        assert 'Invalid type for attribute' in str(context.exception)

        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Graph(
                nodes        = {self.node.node_config.node_id: self.node},
                edges        = {self.edge.edge_config.edge_id: "not-an-edge"},  # Should be Schema__MGraph__Edge
                graph_config = self.graph_config)

        assert str(context.exception) == "Expected a dictionary, but got '<class 'str'>'"

    def test_multiple_nodes_and_edges(self):
        # Create additional test nodes
        node_config_2 = Schema__MGraph__Node_Config(
            node_id    = Random_Guid(),
            node_type  = str,
            value_type = int)
        node_2 = Schema__MGraph__Node(
            attributes  = {},
            node_config = node_config_2,
            value      = 42)

        # Create additional test edge
        edge_config_2 = Schema__MGraph__Edge_Config(
            edge_id        = Random_Guid(),
            from_node_type = str,
            to_node_type   = int)
        edge_2 = Schema__MGraph__Edge(
            attributes   = {},
            edge_config  = edge_config_2,
            from_node_id = self.node.node_config.node_id,
            to_node_id   = node_2.node_config.node_id)

        # Create graph with multiple nodes and edges
        graph = Schema__MGraph__Graph(
            nodes = {
                self.node.node_config.node_id: self.node,
                node_2.node_config.node_id: node_2
            },
            edges = {
                self.edge.edge_config.edge_id: self.edge,
                edge_2.edge_config.edge_id: edge_2
            },
            graph_config = self.graph_config)

        assert len(graph.nodes) == 2
        assert len(graph.edges) == 2
        assert graph.nodes[node_2.node_config.node_id].value == 42