import pytest
from unittest                                 import TestCase
from mgraph_ai.mgraph.actions.MGraph__Storage import MGraph__Storage
from mgraph_ai.mgraph.domain.Domain__MGraph__Graph    import Domain__MGraph__Graph


class test_MGraph__Storage(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mgraph_storage = MGraph__Storage()

    def test_create(self):
        with self.mgraph_storage as _:
            assert _.create()    == _.graph
            assert type(_.graph) is Domain__MGraph__Graph

    def test_delete(self):
        with pytest.raises(NotImplementedError, match="delete applicable to memory only mode") as _:
            self.mgraph_storage.delete()

    def test_safe(self):
        with self.mgraph_storage as _:
            assert _.safe() is True
