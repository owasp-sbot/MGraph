import pytest
from unittest                           import TestCase
from mgraph_ai.domain.MGraph            import MGraph
from osbot_utils.type_safe.Type_Safe    import Type_Safe
from osbot_utils.utils.Misc             import list_set
from osbot_utils.utils.Objects          import base_types
from mgraph_ai.core.MGraphs             import MGraphs
from mgraph_ai.mermaid.Mermaid__Graph   import Mermaid__Graph


class test_Mermaid_MGraph(TestCase):

    @classmethod
    def setUpClass(cls):
        pytest.skip("todo: fix these tests after MGraph refactoring")

    def setUp(self):
        self.mgraph        = MGraphs().new__random(x_nodes=4,y_edges=4)
        self.mermaid_graph = Mermaid__Graph()

    def test__init__(self):
        assert type(self.mermaid_graph) is Mermaid__Graph
        assert base_types(self.mermaid_graph) == [MGraph, Type_Safe, object]
        assert list_set(self.mermaid_graph.__locals__()) == ['config', 'edges', 'key', 'mermaid_code', 'nodes']