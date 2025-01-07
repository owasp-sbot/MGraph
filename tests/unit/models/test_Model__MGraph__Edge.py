from unittest                               import TestCase
from osbot_utils.utils.Misc                 import is_guid
from osbot_utils.utils.Objects              import __
from mgraph_ai.models.Model__MGraph__Edge   import Model__MGraph__Edge
from mgraph_ai.schemas.Schema__MGraph__Edge import Schema__MGraph__Edge

class test_Model__MGraph__Edge(TestCase):

    def setUp(self):
        self.edge = Model__MGraph__Edge()

    def test__init__(self):
        with self.edge.data as _:
            edge_id = _.edge_config.edge_id
            assert type(_) is Schema__MGraph__Edge
            assert _.obj() == __(attributes     = __()                   ,
                                 edge_config=__(edge_id        = edge_id,
                                                from_node_type = None   ,
                                                to_node_type   = None   ),
                                 from_node_id   = _.from_node_id         ,
                                 to_node_id     = _.to_node_id           )
            assert is_guid(edge_id       )
            assert is_guid(_.from_node_id)
            assert is_guid(_.to_node_id  )
