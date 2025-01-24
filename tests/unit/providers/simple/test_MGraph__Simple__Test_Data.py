from unittest                                             import TestCase

from mgraph_ai.mgraph.MGraph import MGraph
from mgraph_ai.providers.simple.MGraph__Simple import MGraph__Simple
from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.utils.Objects import base_types

from mgraph_ai.providers.simple.MGraph__Simple__Test_Data import MGraph__Simple__Test_Data


class test_MGraph__Simple__Test_Data(TestCase):

    def setUp(self):
        self.test_data = MGraph__Simple__Test_Data().create()

    def test_create(self):
        with self.test_data as _:
            assert _.data().nodes_ids() == _.nodes_ids()
            assert _.data().edges_ids() == _.edges_ids()
            assert type(_)              is MGraph__Simple__Test_Data
            assert base_types(_)        == [MGraph__Simple, MGraph, Type_Safe, object]