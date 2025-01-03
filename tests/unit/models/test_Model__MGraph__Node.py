from unittest                             import TestCase
from mgraph_ai.models.Model__MGraph__Node import Model__MGraph__Node


class test_Model__MGraph__Node(TestCase):

    def setUp(self):
        self.node = Model__MGraph__Node()

    def test__init__(self):
        with self.node.data as _:
            assert _.attributes     == {}
            assert _.node_id        == _.node_id
            assert _.node_type      is None