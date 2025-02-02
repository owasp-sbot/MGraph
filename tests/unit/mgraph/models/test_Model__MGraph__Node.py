from unittest                                              import TestCase
from mgraph_db.mgraph.models.Model__MGraph__Node           import Model__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Node         import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data   import Schema__MGraph__Node__Data

class test_Model__MGraph__Node(TestCase):

    def setUp(self):                                                                            # Initialize test data
        self.node_data = Schema__MGraph__Node__Data ()
        self.node      = Schema__MGraph__Node       ( node_data  = self.node_data      ,
                                                      node_type  = Schema__MGraph__Node)
        self.model     = Model__MGraph__Node        ( data       = self.node           )

    def test_init(self):                                                                        # Tests basic initialization
        assert type(self.model)   is Model__MGraph__Node
        assert self.model.data    is self.node