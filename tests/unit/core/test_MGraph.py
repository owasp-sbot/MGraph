from unittest                    import TestCase
from mgraph_ai.core.MGraph__Data import MGraph__Data
from osbot_utils.utils.Objects   import __
from osbot_utils.testing.Stdout  import Stdout
from mgraph_ai.core.MGraph       import MGraph

class test_MGraph(TestCase):

    def setUp(self):
        self.mgraph = MGraph()

    def test___init__(self):
        expected_args = ['config', 'edges', 'key', 'nodes']
        with self.mgraph as _:
            assert _.__attr_names__() == expected_args
            assert _.edges            == []
            assert _.nodes            == {}
            assert _.key.startswith('mgraph_')

    def test_add_node(self):
        with self.mgraph as _:
            new_node = _.new_node()
            assert dict(_.nodes)         == {new_node.node_id : new_node}
            assert new_node.obj()        == __(node_id    = new_node.node_id,
                                               attributes = __()            )

    def test_add_edge(self):
        with self.mgraph as _:
            from_node  = _.new_node()
            to_node    = _.new_node()
            new_edge   = _.add_edge(from_node_id=from_node.node_id, to_node_id=to_node.node_id)
            assert _.edges               == [new_edge]
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
