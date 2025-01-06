from unittest                                      import TestCase
from mgraph_ai.schemas.Schema__MGraph__Edge        import Schema__MGraph__Edge
from mgraph_ai.schemas.Schema__MGraph__Edge_Config import Schema__MGraph__Edge_Config
from mgraph_ai.schemas.Schema__MGraph__Attribute   import Schema__MGraph__Attribute
from osbot_utils.helpers.Random_Guid               import Random_Guid
from osbot_utils.helpers.Safe_Id                   import Safe_Id

class test_Schema__MGraph__Edge(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.from_node_id = Random_Guid()
        cls.to_node_id   = Random_Guid()
        cls.edge_config  = Schema__MGraph__Edge_Config(
            edge_id        = Random_Guid(),
            from_node_type = str,
            to_node_type   = int)

        # Create a sample attribute
        cls.attribute = Schema__MGraph__Attribute(
            attribute_id    = Random_Guid(),
            attribute_name  = Safe_Id('test_attr'),
            attribute_value = "test_value",
            attribute_type  = str)

    def setUp(self):
        self.edge = Schema__MGraph__Edge(
            attributes   = {self.attribute.attribute_id: self.attribute},
            edge_config  = self.edge_config,
            from_node_id = self.from_node_id,
            to_node_id   = self.to_node_id)

    def test__init__(self):
        assert type(self.edge) is Schema__MGraph__Edge
        assert self.edge.from_node_id                            == self.from_node_id
        assert self.edge.to_node_id                              == self.to_node_id
        assert self.edge.edge_config                             == self.edge_config
        assert len(self.edge.attributes)                         == 1
        assert self.edge.attributes[self.attribute.attribute_id] == self.attribute

    def test_type_safety(self):
        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Edge(
                attributes   = "not-a-dict",               # Should be Dict
                edge_config  = self.edge_config,
                from_node_id = self.from_node_id,
                to_node_id   = self.to_node_id)

        assert 'Invalid type for attribute' in str(context.exception)

        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Edge(
                attributes   = {self.attribute.attribute_id: self.attribute},
                edge_config  = "not-an-edge-config",       # Should be Schema__MGraph__Edge_Config
                from_node_id = self.from_node_id,
                to_node_id   = self.to_node_id)

        assert 'Invalid type for attribute' in str(context.exception)

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

        edge = Schema__MGraph__Edge(
            attributes   = {attr_1.attribute_id: attr_1,
                           attr_2.attribute_id: attr_2},
            edge_config  = self.edge_config,
            from_node_id = self.from_node_id,
            to_node_id   = self.to_node_id)

        assert len(edge.attributes) == 2
        assert edge.attributes[attr_1.attribute_id] == attr_1
        assert edge.attributes[attr_2.attribute_id] == attr_2