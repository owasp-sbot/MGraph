from unittest                                                 import TestCase
from mgraph_ai.providers.mermaid.models.Model__Mermaid__Graph import Model__Mermaid__Graph
from osbot_utils.utils.Misc                                   import is_guid
from osbot_utils.utils.Objects                                import __
from mgraph_ai.providers.mermaid.domain.Domain__Mermaid__Edge         import Domain__Mermaid__Edge

class test_Mermaid__Edge(TestCase):

    def setUp(self):
        self.graph        = Model__Mermaid__Graph()
        self.mermaid_edge = Domain__Mermaid__Edge(graph=self.graph)

    def test__init__(self):

        with self.mermaid_edge as _:
            assert type(_) is Domain__Mermaid__Edge
            assert is_guid(_.from_node_id) is True
            assert is_guid(_.to_node_id  ) is True
            assert _.graph                 == self.graph
            assert _.obj()                 == __(edge = __(data=__(label='',
                                                                  edge_config  = __(output_node_from = False,
                                                                                    output_node_to   = False,
                                                                                    edge_mode        = '',
                                                                                    edge_id          = _.edge_config.edge_id),
                                                                  edge_type    = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge.Schema__Mermaid__Edge',
                                                                  edge_data    = __()           ,
                                                                  from_node_id = _.from_node_id ,
                                                                  to_node_id   = _.to_node_id   )),
                                                 graph = self.graph.obj())