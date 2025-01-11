from unittest                                                            import TestCase
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Config  import Schema__Mermaid__Node__Config
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Shape   import Schema__Mermaid__Node__Shape



class test_Schema__Mermaid__Node__Config(TestCase):

    def setUp(self):                                                                # Initialize test data
        self.node_config = Schema__Mermaid__Node__Config(
            markdown         = True                               ,
            node_shape      = Schema__Mermaid__Node__Shape.circle,
            show_label      = True                               ,
            wrap_with_quotes= True
        )

    def test_init(self):                                                            # Tests basic initialization and type checking
        assert type(self.node_config)              is Schema__Mermaid__Node__Config
        assert self.node_config.markdown           is True
        assert self.node_config.node_shape         == Schema__Mermaid__Node__Shape.circle
        assert self.node_config.show_label         is True
        assert self.node_config.wrap_with_quotes   is True

    def test_type_safety_validation(self):                                          # Tests type safety validations
        with self.assertRaises(ValueError) as context:
            Schema__Mermaid__Node__Config(
                markdown         = "not-a-bool"                      ,
                node_shape      = Schema__Mermaid__Node__Shape.circle,
                show_label      = True                               ,
                wrap_with_quotes= True
            )
        assert "Invalid type for attribute" in str(context.exception)

        with self.assertRaises(ValueError) as context:
            Schema__Mermaid__Node__Config(
                markdown         = True                ,
                node_shape      = "not-a-shape"       ,
                show_label      = True                ,
                wrap_with_quotes= True
            )
        assert "Invalid type for attribute" in str(context.exception)


