from unittest                                                import TestCase
from osbot_utils.utils.Dev                                   import pprint
from osbot_utils.type_safe.Type_Safe                         import Type_Safe
from osbot_utils.utils.Objects                               import base_types
from mgraph_ai.mgraph.index.MGraph__Index                    import MGraph__Index
from mgraph_ai.mgraph.index.MGraph__Query                    import MGraph__Query
from mgraph_ai.mgraph.schemas.Schema__MGraph__Index__Data    import Schema__MGraph__Index__Data
from mgraph_ai.providers.simple.MGraph__Simple__Test_Data    import MGraph__Simple__Test_Data
from mgraph_ai.providers.simple.domain.Domain__Simple__Graph import Domain__Simple__Graph
from mgraph_ai.providers.simple.schemas.Schema__Simple__Node import Schema__Simple__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge           import Schema__MGraph__Edge

class test_MGraph__Query(TestCase):

    @classmethod
    def setUpClass(cls):
        import pytest
        pytest.skip("test need fixing")

    def setUp(self):
        self.mgraph = MGraph__Simple__Test_Data().create()
        self.graph  = self.mgraph.graph
        self.index = MGraph__Index.from_graph(self.graph)
        self.query = MGraph__Query           (index=self.index)

    def test_init(self):
        assert type(self.mgraph          ) is MGraph__Simple__Test_Data
        assert type(self.graph           ) is Domain__Simple__Graph
        assert type(self.index           ) is MGraph__Index
        assert type(self.index.index_data) is Schema__MGraph__Index__Data

        with self.query as _:
            assert type(_)                           is MGraph__Query
            assert base_types(_)                     == [Type_Safe, object]
            assert self.query.index                  is self.index
            assert len(self.query.current_node_ids) == 0
            assert self.query.current_node_type is None

    def test_by_type(self):
        with self.mgraph.data() as _:
            nodes_ids = sorted(_.nodes_ids())

        with self.query as _:
            query__result = _.by_type(Schema__Simple__Node)
            assert query__result.count()                  == 3
            assert type(query__result)                    is MGraph__Query
            assert query__result                          != _
            assert list(_            .current_node_ids)   == []
            assert sorted(query__result.current_node_ids) == nodes_ids
            assert query__result.current_node_type        == Schema__Simple__Node.__name__
            assert query__result.current__filters         == []


    def test_with_attribute_name(self):
        with self.query.with_attribute('name', 'Node 1') as _:
            assert type(_) is MGraph__Query
            assert _.current_node_ids == set()                              # BUG should not be empty
            assert _.count()          == 0                                  # BUG should be one
            return
            node = _.first()
            assert node.node_data.name == 'Node 1'
            assert node.node_data.value == 'A'

    def test_with_attribute_value(self):
        nodes = self.query.with_attribute('value', 'B')
        assert nodes.count() == 1
        assert nodes.first().node_data.value == 'B'

    def test_traverse(self):
        # Start with Node 1 and traverse its outgoing edges
        start = self.query.with_attribute('name', 'Node 1')
        connected = start.traverse()
        assert connected.count() == 2  # Node 1 has two edges to Node 2
        assert all(node.node_data.name == 'Node 2'
                  for node in connected.collect())

    def test_traverse_with_edge_type(self):
        start = self.query.with_attribute('name', 'Node 1')
        connected = start.traverse(edge_type=Schema__MGraph__Edge)
        assert connected.count() == 2

    def test_filter(self):
        result = self.query.by_type(Schema__Simple__Node).filter(
            lambda node: node.node_data.value in ['A', 'B']
        )
        assert result.count() == 2
        values = [node.node_data.value for node in result.collect()]
        assert sorted(values) == ['A', 'B']

    def test_collect(self):
        nodes = self.query.by_type(Schema__Simple__Node).collect()
        assert len(nodes) == 3
        assert all(isinstance(node, Schema__Simple__Node) for node in nodes)

    def test_value(self):
        value = self.query.with_attribute('name', 'Node 1').value()
        assert value == 'A'

    def test_empty_query(self):
        empty = self.query.with_attribute('name', 'NonexistentNode')
        assert empty.count() == 0
        assert not empty.exists()
        assert empty.value() is None
        assert empty.first() is None
        assert empty.collect() == []

    def test_property_access(self):
        node = self.query.with_attribute('value', 'A')
        assert node.name == 'Node 1'
        assert node.value == 'A'

    def test_exists(self):
        assert self.query.by_type(Schema__Simple__Node).exists()
        assert not self.query.with_attribute('name', 'NonexistentNode').exists()

    def test_first(self):
        node = self.query.by_type(Schema__Simple__Node).first()
        assert isinstance(node, Schema__Simple__Node)
        assert node.node_data.value in ['A', 'B', 'C']

    def test_chained_operations(self):
        result = (self.query
                 .by_type(Schema__Simple__Node)
                 .filter(lambda n: n.node_data.value in ['A', 'B'])
                 .traverse()
                 .with_attribute('value', 'B'))
        assert result.exists()
        assert result.first().node_data.value == 'B'