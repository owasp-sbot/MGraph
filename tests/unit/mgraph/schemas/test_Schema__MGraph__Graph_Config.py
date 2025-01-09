from unittest                                               import TestCase
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph__Config import Schema__MGraph__Graph__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node          import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge          import Schema__MGraph__Edge
from osbot_utils.helpers.Random_Guid                        import Random_Guid

class Simple_Node(Schema__MGraph__Node): pass    # Helper class for testing

class test__int__Schema__MGraph__Graph__Config(TestCase):

    def setUp(self):    # Initialize test data
        self.graph_id          = Random_Guid()
        self.graph_type        = Schema__MGraph__Graph__Config
        self.graph_config      = Schema__MGraph__Graph__Config(graph_id          = self.graph_id)

    def test_init(self):    # Tests basic initialization and type checking
        assert type(self.graph_config)     is Schema__MGraph__Graph__Config
        assert self.graph_config.graph_id  == self.graph_id

    def test_type_safety_validation(self):    # Tests type safety validations
        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Graph__Config(graph_id="not-a-guid")  # Should be Random_Guid

        assert str(context.exception) == "in Random_Guid: value provided was not a Guid: not-a-guid"
