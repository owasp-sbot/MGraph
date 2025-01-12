from unittest                                               import TestCase
from osbot_utils.helpers.Random_Guid                        import Random_Guid
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config  import Schema__MGraph__Edge__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge          import Schema__MGraph__Edge

class test_Schema__MGraph__Edge(TestCase):

    def setUp(self):    # Initialize test data
        self.from_node_id = Random_Guid()
        self.to_node_id   = Random_Guid()
        self.edge_config  = Schema__MGraph__Edge__Config( edge_id      = Random_Guid()          )
        self.edge        = Schema__MGraph__Edge         ( edge_config  = self.edge_config       ,
                                                          edge_type    = Schema__MGraph__Edge   ,
                                                          from_node_id = self.from_node_id      ,
                                                          to_node_id   = self.to_node_id        )

    def test_init(self):                                                                # Tests basic initialization and type checking
        assert type(self.edge)                                 is Schema__MGraph__Edge
        assert self.edge.from_node_id                          == self.from_node_id
        assert self.edge.to_node_id                            == self.to_node_id
        assert self.edge.edge_config                           == self.edge_config

    def test_type_safety_validation(self):    # Tests type safety validations

        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Edge(edge_config  = "not-an-edge-config",
                                 edge_type    = Schema__MGraph__Edge,
                                 from_node_id = self.from_node_id   ,
                                 to_node_id   = self.to_node_id     )
        assert 'Invalid type for attribute' in str(context.exception)

