from unittest                             import TestCase
from osbot_utils.utils.Misc               import random_int
from mgraph_ai.core.MGraph__Random_Graphs import MGraph__Random_Graphs


class test_MGraph__Random_Graphs(TestCase):

    def setUp(self):
        self.ramdom_graphs = MGraph__Random_Graphs()
        self.config        = self.ramdom_graphs.config

    def test_with_x_nodes_and_y_edges(self):
        self.config.allow_circle_edges    = True            # need to set this or the test below will fail
        self.config.allow_duplicate_edges = True
        x = random_int(max=10)
        y = random_int(max=20)
        new_graph = self.ramdom_graphs.with_x_nodes_and_y_edges(x, y)
        assert type(new_graph).__name__ == 'MGraph'
        assert len(new_graph.nodes)    == x
        assert len(new_graph.edges)    == y

    # @pytest.mark.skip("remove hard coded path")
    # def test_save_graph(self):
    #     # new_graph = self.ramdom_graphs.with_x_nodes_and_y_edges()
    #     # new_graph.data().print()
    #     # saved_graph = pickle_save_to_file(new_graph)
    #     saved_graph = '/var/folders/sj/ks1b_pjd749gk5ssdd1769kc0000gn/T/tmpq_6pkt9p.pickle'
    #     new_graph = pickle_load_from_file(saved_graph)
    #     new_graph.data().print()