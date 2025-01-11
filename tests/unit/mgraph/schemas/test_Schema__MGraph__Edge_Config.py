from unittest                                               import TestCase
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config  import Schema__MGraph__Edge__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node          import Schema__MGraph__Node
from osbot_utils.helpers.Random_Guid                        import Random_Guid

class Simple_Node(Schema__MGraph__Node): pass    # Helper class for testing

class test_Schema__MGraph__Edge__Config(TestCase):

    def setUp(self):    # Initialize test data
        self.edge_id        = Random_Guid()
        self.edge_config    = Schema__MGraph__Edge__Config(edge_id        = self.edge_id)

    def test_init(self):    # Tests basic initialization and type checking
        assert type(self.edge_config) is Schema__MGraph__Edge__Config
        assert self.edge_config.edge_id == self.edge_id

    def test_type_safety_validation(self):    # Tests type safety validations
        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Edge__Config(edge_id="not-a-guid")
        assert str(context.exception) == "in Random_Guid: value provided was not a Guid: not-a-guid"