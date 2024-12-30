from unittest                       import TestCase
from mgraph_ai.core.MGraph__Edge    import MGraph__Edge


class test_MGraph__Edge(TestCase):

    def setUp(self):
        self.edge = MGraph__Edge()

    def test__init__(self):
        assert self.edge.__attr_names__() == sorted(['attributes', 'from_node_id', 'to_node_id', 'from_node_type', 'to_node_type'])

    def test___str__(self):
        assert str(self.edge) == f'[Graph Edge] from "{self.edge.from_node_id}" to "{self.edge.to_node_id}" '