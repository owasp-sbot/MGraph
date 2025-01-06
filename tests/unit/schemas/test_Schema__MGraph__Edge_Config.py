from unittest                                      import TestCase
from mgraph_ai.schemas.Schema__MGraph__Edge_Config import Schema__MGraph__Edge_Config
from osbot_utils.helpers.Random_Guid               import Random_Guid

class test_Schema__MGraph__Edge_Config(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.edge_id        = Random_Guid()
        cls.from_node_type = str
        cls.to_node_type   = int

    def setUp(self):
        self.edge_config = Schema__MGraph__Edge_Config(
            edge_id        = self.edge_id,
            from_node_type = self.from_node_type,
            to_node_type   = self.to_node_type)

    def test__init__(self):
        assert type(self.edge_config)          is Schema__MGraph__Edge_Config
        assert self.edge_config.edge_id        == self.edge_id
        assert self.edge_config.from_node_type == self.from_node_type
        assert self.edge_config.to_node_type   == self.to_node_type

    def test_type_safety(self):
        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Edge_Config(
                edge_id        = "not-a-guid",           # Should be Random_Guid
                from_node_type = self.from_node_type,
                to_node_type   = self.to_node_type)

        assert str(context.exception) == "in Random_Guid: value provided was not a Guid: not-a-guid"

        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Edge_Config(
                edge_id        = self.edge_id,
                from_node_type = "not-a-type",          # Should be type
                to_node_type   = self.to_node_type)

        assert 'Invalid type for attribute' in str(context.exception)

    def test_different_type_combinations(self):
        # Test with built-in types
        edge_config_1 = Schema__MGraph__Edge_Config(
            edge_id        = Random_Guid(),
            from_node_type = bool,
            to_node_type   = list)
        assert edge_config_1.from_node_type == bool
        assert edge_config_1.to_node_type   == list

        # Test with custom class
        class CustomType: pass
        edge_config_2 = Schema__MGraph__Edge_Config(
            edge_id        = Random_Guid(),
            from_node_type = CustomType,
            to_node_type   = dict)
        assert edge_config_2.from_node_type == CustomType
        assert edge_config_2.to_node_type   == dict