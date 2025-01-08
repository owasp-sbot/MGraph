from unittest                                       import TestCase
from mgraph_ai.schemas.Schema__MGraph__Graph_Config import Schema__MGraph__Graph_Config
from mgraph_ai.schemas.Schema__MGraph__Node         import Schema__MGraph__Node
from mgraph_ai.schemas.Schema__MGraph__Edge         import Schema__MGraph__Edge
from osbot_utils.helpers.Random_Guid                import Random_Guid

class Simple_Node(Schema__MGraph__Node): pass    # Helper class for testing

class test__int__Schema__MGraph__Graph_Config(TestCase):

    def setUp(self):    # Initialize test data
        self.graph_id          = Random_Guid()
        self.graph_type        = Schema__MGraph__Graph_Config
        self.default_node_type = Simple_Node
        self.default_edge_type = Schema__MGraph__Edge
        self.graph_config      = Schema__MGraph__Graph_Config(graph_id          = self.graph_id         ,
                                                              default_node_type = self.default_node_type,
                                                              default_edge_type = self.default_edge_type)

    def test_init(self):    # Tests basic initialization and type checking
        assert type(self.graph_config)                 is Schema__MGraph__Graph_Config
        assert self.graph_config.graph_id              == self.graph_id
        assert self.graph_config.default_node_type     == self.default_node_type
        assert self.graph_config.default_edge_type     == self.default_edge_type

    def test_type_safety_validation(self):    # Tests type safety validations
        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Graph_Config(graph_id          = "not-a-guid"          ,     # Should be Random_Guid
                                         default_node_type = self.default_node_type,
                                         default_edge_type = self.default_edge_type )
        assert str(context.exception) == "in Random_Guid: value provided was not a Guid: not-a-guid"

        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Graph_Config(graph_id          = self.graph_id         ,
                                         default_node_type = "not-a-type"         ,     # Should be type
                                         default_edge_type = self.default_edge_type)
        assert 'Invalid type for attribute' in str(context.exception)

    def test_different_node_and_edge_types(self):    # Tests different combinations of node/edge types
        class Another_Node(Schema__MGraph__Node): pass

        graph_config = Schema__MGraph__Graph_Config(graph_id          = Random_Guid()    ,
                                                    default_node_type = Another_Node    ,
                                                    default_edge_type = Schema__MGraph__Edge)
        assert graph_config.default_node_type == Another_Node
        assert graph_config.default_edge_type == Schema__MGraph__Edge