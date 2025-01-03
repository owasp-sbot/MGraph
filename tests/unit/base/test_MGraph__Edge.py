from unittest                       import TestCase
from osbot_utils.utils.Misc         import is_guid
from osbot_utils.utils.Objects      import __
from mgraph_ai.base.MGraph__Edge    import MGraph__Edge

class test_MGraph__Edge(TestCase):

    def setUp(self):
        self.edge = MGraph__Edge()

    def test__init__(self):
        with self.edge as _:
            assert _.obj() == __(attributes     = __()           ,
                                 edge_id        = _.edge_id      ,
                                 from_node_id   = _.from_node_id ,
                                 from_node_type = None           ,
                                 to_node_id     = _.to_node_id   ,
                                 to_node_type   = None           )
            assert is_guid(_.edge_id    )
            assert is_guid(_.from_node_id)
            assert is_guid(_.to_node_id  )
