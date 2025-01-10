from unittest                                                            import TestCase
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Config   import Schema__Mermaid__Node__Config
from osbot_utils.helpers.Random_Guid                                     import Random_Guid
from osbot_utils.helpers.Safe_Id                                         import Safe_Id
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute                  import Schema__MGraph__Attribute
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node           import Schema__Mermaid__Node

class test_Schema__Mermaid__Node(TestCase):

    def setUp(self):                                                                     # Initialize test data
        self.node_config = Schema__Mermaid__Node__Config(node_id         = Random_Guid(),
                                                         value_type      = str)
        self.attribute   = Schema__MGraph__Attribute    (attribute_id    = Random_Guid()   ,
                                                         attribute_name  = Safe_Id('test') ,
                                                         attribute_value = "test_value"    ,
                                                         attribute_type  = str             )
        self.attributes  = {self.attribute.attribute_id: self.attribute}
        self.node        = Schema__Mermaid__Node        (attributes      = self.attributes        ,
                                                         node_config     = self.node_config       ,
                                                         node_type       = Schema__Mermaid__Node  ,
                                                         value           = "test_value"           ,
                                                         key             = Safe_Id("node_1")      ,
                                                         label           = "Test Node"            )

    def test_init(self):                                                            # Tests basic initialization and type checking
        assert type(self.node)                 is Schema__Mermaid__Node
        assert self.node.node_config          == self.node_config
        assert self.node.value                == "test_value"
        assert type(self.node.key)            is Safe_Id
        assert str(self.node.key)             == "node_1"
        assert self.node.label                == "Test Node"
        assert len(self.node.attributes)      == 1

    def test_type_safety_validation(self):                                          # Tests type safety validations
        with self.assertRaises(ValueError) as context:
            Schema__Mermaid__Node(attributes  = self.attributes       ,
                                  node_config = self.node_config      ,
                                  node_type   = 123 ,            # invalid type for note type
                                  value      = "test_value"          ,
                                  key        = 'an-key'                   ,
                                  label      = "Test Node"           )
        assert "Invalid type for attribute 'node_type'" in str(context.exception)

        with self.assertRaises(ValueError) as context:
            Schema__Mermaid__Node(attributes  = self.attributes       ,
                                  node_config = self.node_config      ,
                                  node_type   = Schema__Mermaid__Node ,
                                  value       = "test_value"          ,
                                  key         = Safe_Id("node_1")     ,
                                  label       = 123                   )            # Invalid type for label
        assert "Invalid type for attribute 'label'" in str(context.exception)


    def test_json_serialization(self):                                              # Tests JSON serialization and deserialization
        json_data = self.node.json()

        # Verify JSON structure
        assert 'key'         in json_data
        assert 'label'       in json_data
        assert 'value'       in json_data
        assert 'attributes'  in json_data
        assert 'node_config' in json_data

        # Test deserialization
        restored = Schema__Mermaid__Node.from_json(json_data)
        assert str(restored.key)        == str(self.node.key)
        assert restored.label           == self.node.label
        assert restored.value           == self.node.value
        assert restored.node_type       == self.node.node_type


