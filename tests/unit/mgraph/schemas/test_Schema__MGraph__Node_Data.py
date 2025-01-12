from unittest                                               import TestCase
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data    import Schema__MGraph__Node__Data
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node          import Schema__MGraph__Node
from osbot_utils.helpers.Random_Guid                        import Random_Guid

class Simple_Node(Schema__MGraph__Node): pass           # Helper class for testing

class test_Schema__MGraph__Node__Data(TestCase):

    def setUp(self):    # Initialize test data
        self.node_id    = Random_Guid()
        self.value_type = str
        self.node_config = Schema__MGraph__Node__Data(node_id=self.node_id)

    def test_init(self):                                                                    # Tests basic initialization and type checking
        assert type(self.node_config) is Schema__MGraph__Node__Data
        assert self.node_config.node_id         == self.node_id

    def test_type_safety_validation(self):                                                  # Tests type safety validations
        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Node__Data(node_id    ="not-a-guid")  # Should be Random_Guid

        assert str(context.exception) == "in Random_Guid: value provided was not a Guid: not-a-guid"