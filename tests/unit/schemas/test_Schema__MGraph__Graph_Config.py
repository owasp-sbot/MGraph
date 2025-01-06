from unittest                                       import TestCase
from mgraph_ai.schemas.Schema__MGraph__Graph_Config import Schema__MGraph__Graph_Config
from osbot_utils.helpers.Random_Guid                import Random_Guid

class test__int__Schema__MGraph__Graph_Config(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.graph_id          = Random_Guid()
        cls.graph_type       = dict
        cls.default_node_type = str
        cls.default_edge_type = bool

    def setUp(self):
        self.graph_config = Schema__MGraph__Graph_Config(
            graph_id          = self.graph_id,
            graph_type        = self.graph_type,
            default_node_type = self.default_node_type,
            default_edge_type = self.default_edge_type)

    def test__init__(self):
        assert type(self.graph_config) is Schema__MGraph__Graph_Config
        assert self.graph_config.graph_id          == self.graph_id
        assert self.graph_config.graph_type        == self.graph_type
        assert self.graph_config.default_node_type == self.default_node_type
        assert self.graph_config.default_edge_type == self.default_edge_type

    def test_type_safety(self):
        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Graph_Config(
                graph_id          = "not-a-guid",          # Should be Random_Guid
                graph_type       = self.graph_type,
                default_node_type = self.default_node_type,
                default_edge_type = self.default_edge_type)

        assert str(context.exception) == "in Random_Guid: value provided was not a Guid: not-a-guid"

        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Graph_Config(
                graph_id          = self.graph_id,
                graph_type       = "not-a-type",          # Should be type
                default_node_type = self.default_node_type,
                default_edge_type = self.default_edge_type)

        assert 'Invalid type for attribute' in str(context.exception)

    def test_different_type_configurations(self):
        # Test with different built-in types
        graph_config_1 = Schema__MGraph__Graph_Config(
            graph_id          = Random_Guid(),
            graph_type        = list,
            default_node_type = int,
            default_edge_type = str)
        assert graph_config_1.graph_type        == list
        assert graph_config_1.default_node_type == int
        assert graph_config_1.default_edge_type == str

        # Test with custom class
        class CustomType: pass
        graph_config_2 = Schema__MGraph__Graph_Config(
            graph_id          = Random_Guid(),
            graph_type        = CustomType,
            default_node_type = dict,
            default_edge_type = set)
        assert graph_config_2.graph_type        == CustomType
        assert graph_config_2.default_node_type == dict
        assert graph_config_2.default_edge_type == set