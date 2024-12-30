from unittest                       import TestCase
from mgraph_ai.core.MGraph__Config  import MGraph__Config
from mgraph_ai.core.MGraphs         import MGraphs

class test_MGraphs(TestCase):

    def setUp(self):
        self.MGraphs = MGraphs()
        self.config  = MGraph__Config()


    #@pytest.mark.skip("todo: implement pickle save")
    def test_new__random(self):
        self.config.graph_title = 'Random Graph - from tests'
        mgraph = self.MGraphs.new__random(self.config)
        assert len(mgraph.nodes) == 10
        assert len(mgraph.edges)  > 10
        #pprint(MGraph)
        #MGraph.data().print()
        # saved_graph = MGraph.save()
        # pprint(saved_graph)
        # MGraph_2 = self.MGraphs.load(saved_graph)
        # pprint(MGraph_2)
        # #MGraph_2.print()
    #
    # @pytest.mark.skip("todo: remove hard coded path")
    # def test_load(self):
    #     saved_graph = '/var/folders/sj/ks1b_pjd749gk5ssdd1769kc0000gn/T/tmpo3emajer.pickle'
    #     MGraph = self.MGraphs.load(saved_graph)
    #     MGraph.print()