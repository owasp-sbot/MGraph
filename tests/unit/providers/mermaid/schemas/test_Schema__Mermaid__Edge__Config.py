from unittest                                                           import TestCase
from osbot_utils.helpers.Random_Guid                                    import Random_Guid
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge__Config  import Schema__Mermaid__Edge__Config
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node          import Schema__Mermaid__Node


class test_Schema__Mermaid__Edge__Config(TestCase):

    def setUp(self):                                                                # Initialize test data
        self.edge_id        = Random_Guid()
        self.from_node_type = Schema__Mermaid__Node
        self.to_node_type   = Schema__Mermaid__Node
        self.edge_config    = Schema__Mermaid__Edge__Config(edge_id = self.edge_id)

    def test_init(self):                                                            # Tests basic initialization and type checking
        assert type(self.edge_config)           is Schema__Mermaid__Edge__Config
        assert self.edge_config.edge_id         == self.edge_id

    def test_type_safety_validation(self):                                          # Tests type safety validations
        with self.assertRaises(ValueError) as context:
            Schema__Mermaid__Edge__Config(edge_id = "not-a-guid")
        assert str(context.exception) == "Invalid type for attribute 'edge_id'. Expected '<class 'osbot_utils.helpers.Random_Guid.Random_Guid'>' but got '<class 'str'>'"



