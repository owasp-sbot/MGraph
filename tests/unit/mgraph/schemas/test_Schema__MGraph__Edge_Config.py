from unittest                                               import TestCase
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config  import Schema__MGraph__Edge__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node          import Schema__MGraph__Node
from osbot_utils.helpers.Random_Guid                        import Random_Guid

class Simple_Node(Schema__MGraph__Node): pass    # Helper class for testing

class test_Schema__MGraph__Edge__Config(TestCase):

    def setUp(self):    # Initialize test data
        self.edge_id        = Random_Guid()
        self.from_node_type = Simple_Node
        self.to_node_type   = Simple_Node
        self.edge_config    = Schema__MGraph__Edge__Config(edge_id        = self.edge_id,
                                                           from_node_type = self.from_node_type,
                                                           to_node_type   = self.to_node_type)

    def test_init(self):    # Tests basic initialization and type checking
        assert type(self.edge_config) is Schema__MGraph__Edge__Config
        assert self.edge_config.edge_id        == self.edge_id
        assert self.edge_config.from_node_type == self.from_node_type
        assert self.edge_config.to_node_type   == self.to_node_type

    def test_type_safety_validation(self):    # Tests type safety validations
        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Edge__Config(edge_id        ="not-a-guid",
                                         from_node_type = self.from_node_type,
                                         to_node_type   = self.to_node_type)
        assert str(context.exception) == "in Random_Guid: value provided was not a Guid: not-a-guid"

        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Edge__Config(edge_id        = self.edge_id,
                                         from_node_type = "not-a-type",
                                         to_node_type   = self.to_node_type)
        assert 'Invalid type for attribute' in str(context.exception)

    def test_different_node_types(self):    # Tests different combinations of node types
        class Another_Node(Schema__MGraph__Node): pass

        edge_config = Schema__MGraph__Edge__Config(
            edge_id        = Random_Guid(),
            from_node_type = Simple_Node,
            to_node_type   = Another_Node
        )
        assert edge_config.from_node_type == Simple_Node
        assert edge_config.to_node_type   == Another_Node