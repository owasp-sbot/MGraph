from unittest                                 import TestCase
from mgraph_ai.mgraph.actions.MGraph__Data    import MGraph__Data
from mgraph_ai.mgraph.actions.MGraph__Edit    import MGraph__Edit
from mgraph_ai.mgraph.actions.MGraph__Filter  import MGraph__Filter
from mgraph_ai.mgraph.actions.MGraph__Storage import MGraph__Storage
from mgraph_ai.mgraph.MGraph                  import MGraph

class test_MGraph(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.graph = MGraph()

    def test_data(self):
        with self.graph.data() as _:
            assert type(_) is MGraph__Data
            assert _.graph == self.graph.graph

    def test_edit(self):
        with self.graph.edit() as _:
            assert type(_) is MGraph__Edit
            assert _.graph == self.graph.graph

    def test_storage(self):
        with self.graph.storage() as _:
            assert type(_) is MGraph__Storage
            assert _.graph == self.graph.graph

    def test_filter(self):
        with self.graph.filter() as _:
            assert type(_) is MGraph__Filter
            assert _.graph == self.graph.graph