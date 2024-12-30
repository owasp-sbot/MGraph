from unittest import TestCase

from mgraph_ai.core.MGraph__Edge import MGraph__Edge


class test_MGraph__Edge(TestCase):

    def setUp(self):
        self.edge = MGraph__Edge()

    def test__init__(self):
        assert self.edge.__attr_names__() == ['attributes', 'from_node', 'label', 'to_node']

    def test___str__(self):
        assert str(self.edge) == f'[Graph Edge] from "{self.edge.from_node.key}" to "{self.edge.to_node.key}" '