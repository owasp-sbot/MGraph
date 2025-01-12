from unittest                                              import TestCase
from mgraph_ai.mgraph.models.Model__MGraph__Node           import Model__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node         import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data   import Schema__MGraph__Node__Data
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute    import Schema__MGraph__Attribute
from osbot_utils.helpers.Random_Guid                       import Random_Guid
from osbot_utils.helpers.Safe_Id                           import Safe_Id

class test_Model__MGraph__Node(TestCase):

    def setUp(self):                                                                            # Initialize test data
        self.node_data = Schema__MGraph__Node__Data ( node_id    = Random_Guid()       )
        self.node      = Schema__MGraph__Node       ( attributes = {},
                                                      node_data  = self.node_data      ,
                                                      node_type  = Schema__MGraph__Node)
        self.model     = Model__MGraph__Node        ( data       = self.node           )

    def test_init(self):                                                                        # Tests basic initialization
        assert type(self.model)   is Model__MGraph__Node
        assert self.model.data    is self.node

    def test_attribute_management(self):                                                        # Tests attribute addition and retrieval
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
        retrieved = self.model.attribute(attribute.attribute_id)
        assert retrieved == attribute

        # Test retrieving non-existent attribute
        non_existent = self.model.attribute(Random_Guid())
        assert non_existent is None