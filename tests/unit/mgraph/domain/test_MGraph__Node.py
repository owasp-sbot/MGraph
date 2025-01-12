from unittest                                              import TestCase
from osbot_utils.helpers.Safe_Id                           import Safe_Id
from mgraph_ai.mgraph.domain.Domain__MGraph__Node          import Domain__MGraph__Node
from mgraph_ai.mgraph.models.Model__MGraph__Node           import Model__MGraph__Node
from mgraph_ai.mgraph.models.Model__MGraph__Graph          import Model__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node         import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data   import Schema__MGraph__Node__Data
from osbot_utils.helpers.Random_Guid                       import Random_Guid

class test_MGraph__Node(TestCase):

    def setUp(self):                                                                        # Initialize test data
        self.node_data   = Schema__MGraph__Node__Data(node_id      = Random_Guid())
        self.schema_node = Schema__MGraph__Node       (node_data   = self.node_data,
                                                       node_type   = Schema__MGraph__Node)
        self.model_node = Model__MGraph__Node(data=self.schema_node)
        self.graph      = Model__MGraph__Graph(data=None)                                   # Mock graph for testing
        self.node       = Domain__MGraph__Node(node=self.model_node, graph=self.graph)

    def test_init(self):                                                                    # Tests basic initialization
        assert type(self.node) is Domain__MGraph__Node
        assert self.node.node            is self.model_node
        assert self.node.graph           is self.graph
        assert type(self.node.node_id)  is Random_Guid