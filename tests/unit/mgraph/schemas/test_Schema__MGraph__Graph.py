from unittest                                               import TestCase

from mgraph_ai.mgraph.schemas.Schema__MGraph__Default__Types import Schema__MGraph__Default__Types
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph          import Schema__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph__Config  import Schema__MGraph__Graph__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node           import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Config   import Schema__MGraph__Node__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge           import Schema__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config   import Schema__MGraph__Edge__Config

from osbot_utils.helpers.Random_Guid                        import Random_Guid

class Simple_Node(Schema__MGraph__Node): pass    # Helper class for testing

class test_Schema__MGraph__Graph(TestCase):

    def setUp(self):    # Initialize test data
        self.default_types = Schema__MGraph__Default__Types(node_type      = Simple_Node         ,
                                                            edge_type      = Schema__MGraph__Edge)
        self.graph_config  = Schema__MGraph__Graph__Config (graph_id       = Random_Guid()       )
        self.node_config   = Schema__MGraph__Node__Config  (node_id        = Random_Guid()       ,
                                                            value_type     = str                 )
        self.node          = Schema__MGraph__Node          (attributes     = {}                  ,
                                                            node_config    = self.node_config    ,
                                                            node_type      = Simple_Node         ,
                                                            value          = "test_value"        )
        self.edge_config   = Schema__MGraph__Edge__Config  (edge_id        = Random_Guid()       ,
                                                            from_node_type = Simple_Node         ,
                                                            to_node_type   = Simple_Node         )
        self.edge          = Schema__MGraph__Edge          (attributes     = {}                  ,
                                                            edge_config    = self.edge_config    ,
                                                            edge_type      = Schema__MGraph__Edge,
                                                            from_node_id   = Random_Guid()       ,
                                                            to_node_id     = Random_Guid()       )
        self.graph         = Schema__MGraph__Graph         (default_types  = self.default_types                        ,
                                                            edges          = {self.edge.edge_config.edge_id: self.edge},
                                                            graph_config   = self.graph_config                         ,
                                                            graph_type     = Schema__MGraph__Graph                     ,
                                                            nodes          = {self.node.node_config.node_id: self.node},)

    def test_init(self):    # Tests basic initialization and type checking
        assert type(self.graph)                                    is Schema__MGraph__Graph
        assert self.graph.graph_config                            == self.graph_config
        assert len(self.graph.nodes)                              == 1
        assert len(self.graph.edges)                              == 1
        assert self.graph.nodes[self.node.node_config.node_id]    == self.node
        assert self.graph.edges[self.edge.edge_config.edge_id]    == self.edge

    def test_type_safety_validation(self):    # Tests type safety validations
        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Graph(
                nodes        = "not-a-dict",
                edges        = {self.edge.edge_config.edge_id: self.edge},
                graph_config = self.graph_config,
                graph_type   = Schema__MGraph__Graph
            )
        assert 'Invalid type for attribute' in str(context.exception)

        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Graph(
                nodes        = {self.node.node_config.node_id: self.node},
                edges        = {self.edge.edge_config.edge_id: "not-an-edge"},
                graph_config = self.graph_config,
                graph_type   = Schema__MGraph__Graph
            )
        assert "Expected a dictionary, but got '<class 'str'>'" == str(context.exception)

    def test_multiple_nodes_and_edges(self):    # Tests graph with multiple nodes and edges
        node_config_2 = Schema__MGraph__Node__Config(
            node_id    = Random_Guid(),
            value_type = int
        )
        node_2 = Schema__MGraph__Node(
            attributes  = {},
            node_config = node_config_2,
            node_type   = Simple_Node,
            value      = 42
        )

        edge_config_2 = Schema__MGraph__Edge__Config(
            edge_id        = Random_Guid(),
            from_node_type = Simple_Node,
            to_node_type   = Simple_Node
        )
        edge_2 = Schema__MGraph__Edge(
            attributes   = {},
            edge_config  = edge_config_2,
            edge_type    = Schema__MGraph__Edge,
            from_node_id = self.node.node_config.node_id,
            to_node_id   = node_2.node_config.node_id
        )

        graph = Schema__MGraph__Graph(
            nodes = {
                self.node.node_config.node_id: self.node,
                node_2.node_config.node_id: node_2
            },
            edges = {
                self.edge.edge_config.edge_id: self.edge,
                edge_2.edge_config.edge_id: edge_2
            },
            graph_config = self.graph_config,
            graph_type   = Schema__MGraph__Graph
        )

        assert len(graph.nodes)                                == 2
        assert len(graph.edges)                                == 2
        assert graph.nodes[node_2.node_config.node_id].value  == 42