from unittest                                       import TestCase
from mgraph_ai.mgraph.actions.MGraph__Data          import MGraph__Data
from mgraph_ai.mgraph.domain.MGraph__Graph          import MGraph__Graph
from mgraph_ai.mgraph.models.Model__MGraph__Graph   import Model__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph import Schema__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node  import Schema__MGraph__Node
from osbot_utils.helpers.Random_Guid                import Random_Guid

class Simple_Node(Schema__MGraph__Node): pass  # Helper class for testing

class test_MGraph__Data(TestCase):

    def setUp(self):
        schema_graph = Schema__MGraph__Graph(nodes={}, edges={}, graph_config=None, graph_type=Schema__MGraph__Graph)   # Create a schema graph

        model_graph  = Model__MGraph__Graph(data=schema_graph)                                                          # Create model and domain graph
        domain_graph = MGraph__Graph(model=model_graph)
        self.data    = MGraph__Data(graph=domain_graph)                                                                 # Create data object

    def test_node_and_edge_retrieval(self):
        node1           = self.data.graph.new_node().set_value('node_1')                                                # Create nodes and edges
        node2           = self.data.graph.new_node().set_value('node_2')
        edge            = self.data.graph.new_edge(from_node_id=node1.node_id(), to_node_id=node2.node_id())
        retrieved_node = self.data.node(node1.node_id())                                                                # Test node retrieval

        assert retrieved_node         is not None
        assert retrieved_node.value() == "node_1"

        retrieved_edge = self.data.edge(edge.edge_id())                                                                 # Test edge retrieval
        assert self.data.edges()[0].json()        == edge.json()
        assert self.data.nodes()[0].json()        == node1.json()
        assert self.data.nodes()[1].json()        == node2.json()
        assert retrieved_edge                     is not None
        assert retrieved_edge.from_node().value() == "node_1"
        assert retrieved_edge.to_node  ().value() == "node_2"

    def test_list_nodes_and_edges(self):
        node1 = self.data.graph.new_node()                                                                       # Create multiple nodes and edges
        node2 = self.data.graph.new_node()
        edge  = self.data.graph.new_edge(from_node_id=node1.node_id(), to_node_id=node2.node_id())
        nodes = self.data.graph.nodes()                                                                                 # get nodes list
        edges = self.data.graph.edges()                                                                                 # get edges list

        assert len(nodes)   == 2
        assert node1.json() == nodes[0].json()
        assert node2.json() == nodes[1].json()
        assert len(edges)   == 1
        assert edge.json()  == edges[0].json()

    def test_nonexistent_retrieval(self):
        non_existent_id = Random_Guid()                                                                                 # Test retrieving non-existent node and edge
        assert self.data.node(non_existent_id) is None
        assert self.data.edge(non_existent_id) is None