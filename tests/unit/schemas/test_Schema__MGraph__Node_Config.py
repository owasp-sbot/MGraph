from unittest                                      import TestCase
from mgraph_ai.schemas.Schema__MGraph__Node_Config  import Schema__MGraph__Node_Config
from osbot_utils.helpers.Random_Guid                import Random_Guid

class test_Schema__MGraph__Node_Config(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.node_id    = Random_Guid()
        cls.node_type  = str
        cls.value_type = int

    def setUp(self):
        self.node_config = Schema__MGraph__Node_Config(
            node_id    = self.node_id,
            node_type  = self.node_type,
            value_type = self.value_type)

    def test__init__(self):
        assert type(self.node_config) is Schema__MGraph__Node_Config
        assert self.node_config.node_id    == self.node_id
        assert self.node_config.node_type  == self.node_type
        assert self.node_config.value_type == self.value_type

    def test_type_safety(self):
        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Node_Config(
                node_id    = "not-a-guid",         # Should be Random_Guid
                node_type  = self.node_type,
                value_type = self.value_type)

        assert str(context.exception) == "in Random_Guid: value provided was not a Guid: not-a-guid"

        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Node_Config(
                node_id    = self.node_id,
                node_type  = "not-a-type",         # Should be type
                value_type = self.value_type)

        assert 'Invalid type for attribute' in str(context.exception)

        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Node_Config(
                node_id    = self.node_id,
                node_type  = self.node_type,
                value_type = "not-a-type")         # Should be type

        assert 'Invalid type for attribute' in str(context.exception)

    def test_different_type_combinations(self):
        # Test with built-in types
        node_config_1 = Schema__MGraph__Node_Config(
            node_id    = Random_Guid(),
            node_type  = dict,
            value_type = list)
        assert node_config_1.node_type  == dict
        assert node_config_1.value_type == list

        # Test with custom class
        class CustomNodeType: pass
        class CustomValueType: pass

        node_config_2 = Schema__MGraph__Node_Config(
            node_id    = Random_Guid(),
            node_type  = CustomNodeType,
            value_type = CustomValueType)
        assert node_config_2.node_type  == CustomNodeType
        assert node_config_2.value_type == CustomValueType

        # Test with same type for node and value
        node_config_3 = Schema__MGraph__Node_Config(
            node_id    = Random_Guid(),
            node_type  = str,
            value_type = str)
        assert node_config_3.node_type  == str
        assert node_config_3.value_type == str