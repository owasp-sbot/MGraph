from unittest                                       import TestCase
from mgraph_ai.schemas.Schema__MGraph__Node         import Schema__MGraph__Node
from mgraph_ai.schemas.Schema__MGraph__Node_Config  import Schema__MGraph__Node_Config
from mgraph_ai.schemas.Schema__MGraph__Attribute    import Schema__MGraph__Attribute
from osbot_utils.helpers.Random_Guid                import Random_Guid
from osbot_utils.helpers.Safe_Id                    import Safe_Id

class test_Schema__MGraph__Node(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.node_config = Schema__MGraph__Node_Config(
            node_id    = Random_Guid(),
            node_type  = str,
            value_type = str)

        # Create a sample attribute
        cls.attribute = Schema__MGraph__Attribute(
            attribute_id    = Random_Guid(),
            attribute_name  = Safe_Id('test_attr'),
            attribute_value = "test_value",
            attribute_type  = str)

    def setUp(self):
        self.node = Schema__MGraph__Node(
            attributes  = {self.attribute.attribute_id: self.attribute},
            node_config = self.node_config,
            value      = "test_node_value")

    def test__init__(self):
        assert type(self.node) is Schema__MGraph__Node
        assert self.node.node_config == self.node_config
        assert self.node.value == "test_node_value"
        assert len(self.node.attributes) == 1
        assert self.node.attributes[self.attribute.attribute_id] == self.attribute

    def test_type_safety(self):
        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Node(
                attributes  = "not-a-dict",            # Should be Dict
                node_config = self.node_config,
                value      = "test_node_value")

        assert 'Invalid type for attribute' in str(context.exception)

        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Node(attributes  = {self.attribute.attribute_id: self.attribute},
                                 node_config = "not-a-node-config",     # Should be Schema__MGraph__Node_Config
                                 value      = "test_node_value")

        assert 'Invalid type for attribute' in str(context.exception)

    def test_different_value_types(self):
        # Test with integer value
        node_config_int = Schema__MGraph__Node_Config(
            node_id    = Random_Guid(),
            node_type  = str,
            value_type = int)

        node_int = Schema__MGraph__Node(
            attributes  = {},
            node_config = node_config_int,
            value      = 42)
        assert node_int.value == 42

        # Test with boolean value
        node_config_bool = Schema__MGraph__Node_Config(
            node_id    = Random_Guid(),
            node_type  = str,
            value_type = bool)

        node_bool = Schema__MGraph__Node(
            attributes  = {},
            node_config = node_config_bool,
            value      = True)
        assert node_bool.value is True

    def test_multiple_attributes(self):
        attr_1 = Schema__MGraph__Attribute(
            attribute_id    = Random_Guid(),
            attribute_name  = Safe_Id('attr_1'),
            attribute_value = "value_1",
            attribute_type  = str)

        attr_2 = Schema__MGraph__Attribute(
            attribute_id    = Random_Guid(),
            attribute_name  = Safe_Id('attr_2'),
            attribute_value = 42,
            attribute_type  = int)

        node = Schema__MGraph__Node(
            attributes  = {
                attr_1.attribute_id: attr_1,
                attr_2.attribute_id: attr_2
            },
            node_config = self.node_config,
            value      = "test_node_value")

        assert len(node.attributes) == 2
        assert node.attributes[attr_1.attribute_id] == attr_1
        assert node.attributes[attr_2.attribute_id] == attr_2