from unittest                               import TestCase
from osbot_utils.utils.Objects              import __
from mgraph_ai.models.Model__MGraph__Node   import Model__MGraph__Node


class test_Model__MGraph__Node(TestCase):

    def setUp(self):
        self.node = Model__MGraph__Node()

    def test__init__(self):
        with self.node.data as _:
            node_id = _.node_config.node_id
            assert _.obj() == __(attributes=__(),
                                 node_config=__(node_id    = node_id,
                                                node_type  = None   ,
                                                value_type = None   ),
                                 value=None)