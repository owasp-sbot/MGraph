import pytest
from unittest                                import TestCase
from mgraph_ai.domain.MGraph                 import MGraph
from mgraph_ai.schemas.Schema__MGraph__Edge  import Schema__MGraph__Edge
from osbot_utils.utils.Misc                  import is_guid
from mgraph_ai.core.MGraph__Data             import MGraph__Data
from mgraph_ai.schemas.Schema__MGraph__Graph import Schema__MGraph__Graph
from osbot_utils.utils.Objects               import __
from osbot_utils.testing.Stdout              import Stdout


class test__todo__MGraph(TestCase):

    @classmethod
    def setUpClass(cls):
        pytest.skip("todo: fix these tests after MGraph refactoring")

    def setUp(self):
        self.mgraph = MGraph()

    def test___init__(self):
        expected_args = ['config', 'data']
        with self.mgraph as _:
            assert _.__attr_names__() == expected_args
        with self.mgraph.data as _:
            assert type(_)             is Schema__MGraph__Graph
            assert _.edges             == {}
            assert _.nodes             == {}
            assert is_guid(_.graph_id) is True

    def test_add_node(self):
        with self.mgraph as _:
            new_node = _.new_node()
            assert dict(_.nodes())       == {new_node.node_id : new_node}
            assert new_node.obj()        == __(attributes = __()            ,
                                               node_id    = new_node.node_id,
                                               node_type  = None            )

    def test_add_edge(self):
        with self.mgraph as _:
            from_node  = _.new_node()
            to_node    = _.new_node()
            new_edge   = _.add_edge(from_node_id=from_node.node_id, to_node_id=to_node.node_id)
            assert type(new_edge) is Schema__MGraph__Edge
            assert _.edges().json()     == {new_edge.edge_id: new_edge.json()}

            assert new_edge.from_node_id == from_node.node_id
            assert new_edge.to_node_id   == to_node.node_id
            assert new_edge.__locals__() == dict(attributes     = {}                ,
                                                 edge_id        =  new_edge.edge_id ,
                                                 from_node_id   =  from_node.node_id,
                                                 from_node_type = None              ,
                                                 to_node_id     =  to_node.node_id  ,
                                                 to_node_type   = None              )

            with Stdout() as stdout:
                print()
                MGraph__Data(graph=_).print()

            assert stdout.value() == ('\n'
                                      '\n'
                                      '┌─────────────────────────────────────────────────────────────────────────────────┐\n'
                                      '│ key                                  │ edges                                    │\n'
                                      '├─────────────────────────────────────────────────────────────────────────────────┤\n'
                                     f"│ {from_node.node_id} │ ['{to_node.node_id}'] │\n"
                                     f'│ {to_node  .node_id} │ []                                       │\n'
                                      '└─────────────────────────────────────────────────────────────────────────────────┘\n')
