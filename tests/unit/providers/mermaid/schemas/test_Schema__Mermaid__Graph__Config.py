from unittest                                                           import TestCase
from osbot_utils.helpers.Random_Guid                                    import Random_Guid
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge          import Schema__Mermaid__Edge
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Graph__Config import Schema__Mermaid__Graph__Config
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node          import Schema__Mermaid__Node


class test_Schema__Mermaid__Graph__Config(TestCase):

    def setUp(self):                                                                # Initialize test data
        self.graph_config = Schema__Mermaid__Graph__Config(
            graph_id             = Random_Guid()        ,
            default_node_type    = Schema__Mermaid__Node,
            default_edge_type    = Schema__Mermaid__Edge,
            allow_circle_edges   = True                 ,
            allow_duplicate_edges= False                ,
            graph_title         = "Test Graph"
        )

    def test_init(self):                                                            # Tests basic initialization and type checking
        assert type(self.graph_config)                    is Schema__Mermaid__Graph__Config
        assert self.graph_config.default_node_type        == Schema__Mermaid__Node
        assert self.graph_config.default_edge_type        == Schema__Mermaid__Edge
        assert self.graph_config.allow_circle_edges       is True
        assert self.graph_config.allow_duplicate_edges    is False
        assert self.graph_config.graph_title             == "Test Graph"

    def test_type_safety_validation(self):                                          # Tests type safety validations
        with self.assertRaises(ValueError) as context:
            Schema__Mermaid__Graph__Config(graph_id             = "not-a-guid"        , # invalid guid
                                           default_node_type    = Schema__Mermaid__Node,
                                           default_edge_type    = Schema__Mermaid__Edge,
                                           allow_circle_edges   = True                 ,
                                           allow_duplicate_edges= False                ,
                                           graph_title         = "Test Graph"          )
        assert str(context.exception) == "Invalid type for attribute 'graph_id'. Expected '<class 'osbot_utils.helpers.Random_Guid.Random_Guid'>' but got '<class 'str'>'"

        with self.assertRaises(ValueError) as context:
            Schema__Mermaid__Graph__Config(graph_id             = Random_Guid()       ,
                                          default_node_type    = Schema__Mermaid__Node,
                                          default_edge_type    = Schema__Mermaid__Edge,
                                          allow_circle_edges   = True                 ,
                                          allow_duplicate_edges= False                ,
                                          graph_title          = 123                  ) # Invalid type for title

        assert "Invalid type for attribute" in str(context.exception)

