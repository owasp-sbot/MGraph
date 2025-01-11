from unittest                                             import TestCase
from mgraph_ai.providers.mermaid.actions.Mermaid__Data    import Mermaid__Data
from mgraph_ai.providers.mermaid.utils.Test_Data__Mermaid import Test_Data_Mermaid

# todo: refactor this out with Mermaid__Random_Graph

class test_Mermaid__Data(TestCase):

    def setUp(self):                                                                # Initialize test data
        test_data = Test_Data_Mermaid.create_test_graph()
        self.graph      = test_data['graph']
        self.graph_data = test_data['graph_data']
        self.node_keys  = test_data['node_keys']
        self.nodes      = test_data['nodes']
        self.data       = Mermaid__Data(graph=self.graph)

    def test_init(self):                                                            # Tests basic initialization
        assert isinstance(self.data, Mermaid__Data)
        assert self.data.graph == self.graph

    def test_nodes__by_key(self):                                                  # Tests node retrieval by key
        nodes_dict = self.data.nodes__by_key()

        assert len(nodes_dict) == len(self.nodes)
        for node, key in zip(self.nodes, self.node_keys):
            assert nodes_dict[key].node.data == node.data

    def test_nodes__keys(self):                                                    # Tests key retrieval
        keys = self.data.nodes__keys()

        assert len(keys) == len(self.node_keys)
        assert sorted(keys) == sorted(self.node_keys)

    def test_empty_graph(self):                                                    # Tests behavior with empty graph
        empty_data = Test_Data_Mermaid.create_empty_graph()
        empty_data_instance = Mermaid__Data(graph=empty_data['graph'])

        assert len(empty_data_instance.nodes__by_key()) == 0
        assert len(empty_data_instance.nodes__keys  ()) == 0

    def test_inherited_methods(self):                                              # Tests inherited MGraph__Data methods
        assert len(self.data.nodes()) == len(self.nodes)
        assert len(self.data.edges()) == 0