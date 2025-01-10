import pytest
from unittest                                         import TestCase
from osbot_utils.utils.Misc                           import is_guid
from osbot_utils.utils.Objects                        import __
from mgraph_ai.providers.mermaid.domain.Mermaid       import Mermaid
from mgraph_ai.providers.mermaid.domain.Mermaid__Node import Mermaid__Node
from mgraph_ai.providers.mermaid.domain.Mermaid__Edge import Mermaid__Edge

class test_Mermaid_Edge(TestCase):

    @classmethod
    def setUpClass(cls):
        pytest.skip("todo: fix these tests after MGraph refactoring")

    def setUp(self):
        self.mermaid_edge = Mermaid__Edge()

    def test__init__(self):

        with self.mermaid_edge as _:
            assert type(_)                 is Mermaid__Edge
            assert is_guid(_.from_node_id  ) is True
            assert is_guid(_.to_node_id    ) is True
            assert type   (_.from_node_type) is type
            assert type   (_.to_node_type  ) is type
            assert _.from_node_type          is Mermaid__Node
            assert _.to_node_type            is Mermaid__Node
            assert _.obj()                 == __(config         = __(output_node_from = False                   ,
                                                                     output_node_to   = False                   ,
                                                                     edge_mode        = ''                      ),
                                                 label          = ''                                             ,
                                                 attributes     = __()                                           ,
                                                 edge_id        = _.edge_id                                      ,
                                                 from_node_id   = _.from_node_id                                 ,
                                                 from_node_type = 'mgraph_ai.mermaid.domain.Mermaid__Node.Mermaid__Node',
                                                 to_node_id     = _.to_node_id                ,
                                                 to_node_type   = 'mgraph_ai.mermaid.domain.Mermaid__Node.Mermaid__Node')

    def test__config__edge__output_node_from(self):
        with Mermaid() as _:
            new_edge = _.add_edge('id', 'id2').output_node_from()
            assert _.code()                             == 'graph LR\n    id["id"]\n    id2["id2"]\n\n    id["id"] --> id2'
            assert new_edge.config.output_node_from     is True
            assert _.render().render_edge(new_edge) == '    id["id"] --> id2'
            new_edge.output_node_from(False)
            assert new_edge.config.output_node_from     is False
            assert _.render().render_edge(new_edge) == '    id --> id2'