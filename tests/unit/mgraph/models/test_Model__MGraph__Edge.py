from unittest                                              import TestCase
from mgraph_ai.mgraph.models.Model__MGraph__Edge           import Model__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge         import Schema__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config import Schema__MGraph__Edge__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node         import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute    import Schema__MGraph__Attribute
from osbot_utils.helpers.Random_Guid                       import Random_Guid
from osbot_utils.helpers.Safe_Id                           import Safe_Id

class test_Model__MGraph__Edge(TestCase):

    def setUp(self):    # Initialize test data
        self.from_node_id = Random_Guid()
        self.to_node_id   = Random_Guid()
        self.edge_config  = Schema__MGraph__Edge__Config(edge_id        = Random_Guid())
        self.edge = Schema__MGraph__Edge(
            attributes   = {},
            edge_config  = self.edge_config,
            edge_type    = Schema__MGraph__Edge,
            from_node_id = self.from_node_id,
            to_node_id   = self.to_node_id
        )
        self.model = Model__MGraph__Edge(data=self.edge)

    def test_init(self):    # Tests basic initialization
        assert type(self.model)         is Model__MGraph__Edge
        assert self.model.data          is self.edge
        assert self.model.from_node_id() == self.from_node_id
        assert self.model.to_node_id()   == self.to_node_id

    def test_attribute_management(self):    # Tests attribute addition and retrieval
        attribute = Schema__MGraph__Attribute(
            attribute_id    = Random_Guid(),
            attribute_name  = Safe_Id('test_attr'),
            attribute_value = "attr_value",
            attribute_type  = str
        )

        # Test adding attribute
        self.model.add_attribute(attribute)
        assert len(self.model.data.attributes) == 1

        # Test retrieving attribute
        retrieved = self.model.get_attribute(attribute.attribute_id)
        assert retrieved == attribute

        # Test retrieving non-existent attribute
        non_existent = self.model.get_attribute(Random_Guid())
        assert non_existent is None

    def test_node_ids(self):    # Tests node ID getters
        assert self.model.from_node_id() == self.from_node_id
        assert self.model.to_node_id()   == self.to_node_id