from unittest                                                           import TestCase
from mgraph_ai.mgraph.models.Model__MGraph__Edge                        import Model__MGraph__Edge
from mgraph_ai.mgraph.models.Model__MGraph__Node                        import Model__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph                     import Schema__MGraph__Graph
from osbot_utils.helpers.Random_Guid                                    import Random_Guid
from mgraph_ai.providers.mermaid.models.Model__Mermaid__Graph           import Model__Mermaid__Graph
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Graph         import Schema__Mermaid__Graph
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Graph__Config import Schema__Mermaid__Graph__Config
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node          import Schema__Mermaid__Node
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge          import Schema__Mermaid__Edge
from mgraph_ai.mgraph.models.Model__MGraph__Graph                       import Model__MGraph__Graph

class test_Model__Mermaid__Graph(TestCase):

    def setUp(self):                                                                # Initialize test data
        self.graph_config = Schema__Mermaid__Graph__Config (graph_id              = Random_Guid(),
                                                            allow_circle_edges    =  True        ,
                                                            allow_duplicate_edges = False        ,
                                                            graph_title           = "Test Graph" )

        self.graph_data  = Schema__Mermaid__Graph          (edges         = {},
                                                            nodes         = {},
                                                            graph_config  = self.graph_config,
                                                            graph_type    = Schema__Mermaid__Graph,
                                                            mermaid_code  = [])

        self.graph = Model__Mermaid__Graph(data=self.graph_data)

    def test_init(self):                                                            # Tests basic initialization
        assert type          (self.graph) is Model__Mermaid__Graph
        assert isinstance    (self.graph, Model__MGraph__Graph)                     # Should inherit from MGraph
        assert isinstance    (self.graph.data, Schema__Mermaid__Graph)              # Should use Mermaid schema

        assert type(self.graph.data) is not  Schema__MGraph__Graph                  # Should be exact type match
        assert type(self.graph.data) is      Schema__Mermaid__Graph                 # Should be exact type match

    def test_node_operations(self):                                                # Tests node operations with Mermaid types
        # Create a node with Mermaid-specific attributes
        node = self.graph.new_node(node_type=Schema__Mermaid__Node)

        # Verify node type and inheritance
        assert isinstance(node, Model__MGraph__Node)                               # Should satisfy MGraph interface
        assert isinstance(node.data, Schema__Mermaid__Node)                       # Should use Mermaid schema

        # Test node retrieval
        node_id = node.node_id
        retrieved_node = self.graph.node(node_id)
        assert isinstance(retrieved_node, Model__MGraph__Node)
        assert isinstance(retrieved_node.data, Schema__Mermaid__Node)

        # Test nodes iteration
        nodes = list(self.graph.nodes())
        assert len(nodes) == 1
        assert isinstance(nodes[0], Model__MGraph__Node)
        assert isinstance(nodes[0].data, Schema__Mermaid__Node)

    def test_edge_operations(self):                                                # Tests edge operations with Mermaid types
        # Create two nodes to connect
        node1 = self.graph.new_node(node_type=Schema__Mermaid__Node)
        node2 = self.graph.new_node(node_type=Schema__Mermaid__Node)

        # Create edge between nodes
        edge = self.graph.new_edge(from_node_id = node1.node_id,
                                   to_node_id   = node2.node_id)

        # Verify edge type and inheritance
        assert isinstance(edge, Model__MGraph__Edge)                               # Should satisfy MGraph interface
        assert isinstance(edge.data, Schema__Mermaid__Edge)                       # Should use Mermaid schema

        # Test edge retrieval
        edge_id = edge.edge_id()
        retrieved_edge = self.graph.edge(edge_id)
        assert isinstance(retrieved_edge, Model__MGraph__Edge)
        assert isinstance(retrieved_edge.data, Schema__Mermaid__Edge)

        # Test edges iteration
        edges = list(self.graph.edges())
        assert len(edges) == 1
        assert isinstance(edges[0], Model__MGraph__Edge)
        assert isinstance(edges[0].data, Schema__Mermaid__Edge)

    def test_mermaid_specific_config(self):                                        # Tests Mermaid-specific configuration
        assert hasattr(self.graph.data.graph_config, 'allow_circle_edges')
        assert hasattr(self.graph.data.graph_config, 'allow_duplicate_edges')
        assert hasattr(self.graph.data.graph_config, 'graph_title')

        assert self.graph.data.graph_config.allow_circle_edges is True
        assert self.graph.data.graph_config.allow_duplicate_edges is False
        assert self.graph.data.graph_config.graph_title == "Test Graph"

    def test_mermaid_code_list(self):                                             # Tests Mermaid-specific mermaid_code list
        assert hasattr(self.graph.data, 'mermaid_code')
        assert isinstance(self.graph.data.mermaid_code, list)

        # Initial state should be empty
        assert len(self.graph.data.mermaid_code) == 0