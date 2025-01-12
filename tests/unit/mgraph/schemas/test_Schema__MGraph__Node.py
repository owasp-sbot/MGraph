from unittest                                            import TestCase
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node       import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data import Schema__MGraph__Node__Data
from osbot_utils.helpers.Random_Guid                     import Random_Guid

class test_Schema__MGraph__Node(TestCase):

    def setUp(self):    # Initialize test data
        self.node_data  = Schema__MGraph__Node__Data(node_id        = Random_Guid()       )

        self.node      = Schema__MGraph__Node      (node_data       = self.node_data      ,
                                                    node_type       = Schema__MGraph__Node)

    def test_init(self):                                                                            # Tests basic initialization and type checking
        assert type(self.node)                                  is Schema__MGraph__Node
        assert self.node.node_data == self.node_data

    def test_type_safety_validation(self):                                                          # Tests type safety validations

        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Node(node_data   = "not-a-node-config"                         ,        # Should be Schema__MGraph__Node__Config
                                 node_type   = Schema__MGraph__Node                        )
        assert 'Invalid type for attribute' in str(context.exception)