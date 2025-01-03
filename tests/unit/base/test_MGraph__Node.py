from unittest                    import TestCase
from osbot_utils.utils.Misc      import random_guid
from mgraph_ai.base.MGraph__Node import MGraph__Node


class test_MGraph__Node(TestCase):

    def setUp(self):
        self.node = MGraph__Node()

    def test__init__(self):
        assert self.node.__attr_names__() == ['attributes','node_id']

    def test___str__(self):
        new_id = random_guid()
        self.node.node_id = new_id

    def test_json(self):
        assert self.node.json() == {'attributes': {}                ,
                                    'node_id'   : self.node.node_id }