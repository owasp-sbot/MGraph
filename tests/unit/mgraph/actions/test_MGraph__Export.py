from unittest                                       import TestCase
from mgraph_ai.mgraph.MGraph                        import MGraph
from mgraph_ai.mgraph.utils.MGraph__Static__Graph   import MGraph__Static__Graph
from osbot_utils.utils.Objects                      import obj, __

class test_MGraph__Export(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.linear_graph = MGraph__Static__Graph.create_linear()


    def test_to__mgraph_json(self):
        empty_graph = MGraph()
        data        = empty_graph.export().to__mgraph_json()
        assert data      == empty_graph.graph.model.data.json()
        assert obj(data) == __(edges        =__()                                                                   ,
                               graph_data   =__()                                                                   ,
                               graph_id     = empty_graph.data().graph_id()                                         ,
                               graph_type   ='mgraph_ai.mgraph.schemas.Schema__MGraph__Graph.Schema__MGraph__Graph' ,
                               nodes        = __()                                                                  ,
                               schema_types = __(edge_type        = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Edge.Schema__MGraph__Edge',
                                                 edge_config_type = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config.Schema__MGraph__Edge__Config',
                                                 graph_data_type  = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Graph__Data.Schema__MGraph__Graph__Data',
                                                 node_type        = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Node.Schema__MGraph__Node',
                                                 node_data_type   = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data.Schema__MGraph__Node__Data'))

    def test_to__json(self):
        node_ids = self.linear_graph.node_ids
        edge_ids = self.linear_graph.edge_ids
        with self.linear_graph.graph.export() as _:
            assert _.to__json() == _.to__json() == {'edges': { edge_ids[0]: {'from_node_id': node_ids[0]  ,       # {1st edge}: from {1st node}
                                                                                   'to_node_id'  : node_ids[1]  },      #           : to   {2nd node}
                                                                     edge_ids[1]: {'from_node_id': node_ids[1]  ,       # {2nd edge}: from {2nd node}
                                                                                   'to_node_id'  : node_ids[2]  }},     #           : to   {3rd node}
                                                          'nodes': { node_ids[0]: {},                                   # 1st node
                                                                     node_ids[1]: {},                                   # 2nd node
                                                                     node_ids[2]: {}}}                                  # 3rd node

