from unittest                                                import TestCase
from mgraph_db.mgraph.schemas.Schema__MGraph__Types          import Schema__MGraph__Types
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph          import Schema__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data    import Schema__MGraph__Graph__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Node           import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data     import Schema__MGraph__Node__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge           import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge__Config   import Schema__MGraph__Edge__Config
from osbot_utils.helpers.Obj_Id import Obj_Id


class Simple_Node(Schema__MGraph__Node): pass    # Helper class for testing

class test_Schema__MGraph__Graph(TestCase):

    def setUp(self):    # Initialize test data
        self.schema_types  = Schema__MGraph__Types(node_type      = Simple_Node,
                                                   edge_type      = Schema__MGraph__Edge)
        self.graph_data   = Schema__MGraph__Graph__Data   ()
        self.node_data     = Schema__MGraph__Node__Data    ()
        self.node          = Schema__MGraph__Node          (node_data      = self.node_data,
                                                            node_type      = Simple_Node)
        self.edge_config   = Schema__MGraph__Edge__Config  (edge_id        = Obj_Id()            )
        self.edge          = Schema__MGraph__Edge          (edge_config    = self.edge_config    ,
                                                            edge_type      = Schema__MGraph__Edge,
                                                            from_node_id   = Obj_Id()            ,
                                                            to_node_id     = Obj_Id()            )
        self.graph         = Schema__MGraph__Graph         (schema_types   = self.schema_types,
                                                            edges          = {self.edge.edge_config.edge_id: self.edge},
                                                            graph_data     = self.graph_data,
                                                            graph_type     = Schema__MGraph__Graph,
                                                            nodes          = {self.node.node_id: self.node}, )

    def test_init(self):    # Tests basic initialization and type checking
        assert type(self.graph)                                is Schema__MGraph__Graph
        assert self.graph.graph_data == self.graph_data
        assert len(self.graph.nodes)                           == 1
        assert len(self.graph.edges)                           == 1
        assert self.graph.nodes[self.node.node_id            ] == self.node
        assert self.graph.edges[self.edge.edge_config.edge_id] == self.edge

    def test_type_safety_validation(self):    # Tests type safety validations
        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Graph(
                nodes        = "not-a-dict",
                edges        = {self.edge.edge_config.edge_id: self.edge},
                graph_config = self.graph_data,
                graph_type   = Schema__MGraph__Graph
            )
        assert 'Invalid type for attribute' in str(context.exception)

        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Graph(
                nodes        = {self.node.node_id            : self.node    },
                edges        = {self.edge.edge_config.edge_id: "not-an-edge"},
                graph_config = self.graph_data,
                graph_type   = Schema__MGraph__Graph
            )
        assert "Expected a dictionary, but got '<class 'str'>'" == str(context.exception)

    def test_multiple_nodes_and_edges(self):    # Tests graph with multiple nodes and edges
        node_data_2   = Schema__MGraph__Node__Data  (                                    )
        node_2        = Schema__MGraph__Node        (node_data    = node_data_2          )
        edge_config_2 = Schema__MGraph__Edge__Config(edge_id      = Obj_Id()             )
        edge_2        = Schema__MGraph__Edge        (edge_config  = edge_config_2        ,
                                                     edge_type    = Schema__MGraph__Edge ,
                                                     from_node_id = self.node.node_id    ,
                                                     to_node_id   = node_2.node_id       )

        graph = Schema__MGraph__Graph               (nodes        = { self.node.node_id : self.node             ,
                                                                      node_2.node_id    : node_2               },
                                                     edges        = { self.edge.edge_config.edge_id : self.edge ,
                                                                      edge_2.edge_config.edge_id    : edge_2   },
                                                     graph_data   = self.graph_data                             ,
                                                     graph_type   = Schema__MGraph__Graph                       )

        assert len(graph.nodes) == 2
        assert len(graph.edges) == 2