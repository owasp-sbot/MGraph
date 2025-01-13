from unittest                                                            import TestCase
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Default__Types import Schema__Mermaid__Default__Types
from osbot_utils.helpers.Random_Guid                                     import Random_Guid
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Graph__Config  import Schema__Mermaid__Graph__Config

class test_Schema__Mermaid__Graph__Config(TestCase):

    def setUp(self):                                                                # Initialize test data
        self.schema_types  = Schema__Mermaid__Default__Types()
        self.graph_config  = Schema__Mermaid__Graph__Config(allow_circle_edges   = True       ,
                                                            allow_duplicate_edges= False      ,
                                                            graph_title         = "Test Graph")

    def test_init(self):                                                            # Tests basic initialization and type checking
        assert type(self.graph_config)                 is Schema__Mermaid__Graph__Config
        assert self.schema_types.graph_data_type       is Schema__Mermaid__Graph__Config
        assert self.graph_config.allow_circle_edges    is True
        assert self.graph_config.allow_duplicate_edges is False
        assert self.graph_config.graph_title           == "Test Graph"


    def test_type_safety_validation(self):                                          # Tests type safety validations
        with self.assertRaises(ValueError) as context:
            Schema__Mermaid__Graph__Config(allow_circle_edges   = True ,
                                           allow_duplicate_edges= False,
                                           graph_title          = 123  ) # Invalid type for title

        assert "Invalid type for attribute" in str(context.exception)

