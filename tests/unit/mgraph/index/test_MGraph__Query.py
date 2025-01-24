from unittest                                               import TestCase

import pytest

from mgraph_ai.mgraph.index.MGraph__Index                   import MGraph__Index
from mgraph_ai.mgraph.index.MGraph__Query import Graph__Query
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph         import Schema__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node          import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data    import Schema__MGraph__Node__Data
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge          import Schema__MGraph__Edge
from osbot_utils.helpers.Random_Guid                        import Random_Guid

# Helper classes for testing
class Schema__Test__Node(Schema__MGraph__Node):
    node_data: Schema__MGraph__Node__Data

# todo: replace this with an  MGraph__Simple object
class Graph__Query__Test:
    @classmethod
    def create_test_graph(cls) -> tuple[Schema__MGraph__Graph, MGraph__Index]:
        # Create test graph with known structure
        graph = Schema__MGraph__Graph()
        index = MGraph__Index(graph=graph)

        # Create nodes
        user_node   = Schema__Test__Node(node_id=Random_Guid(), value='john')
        name_node   = Schema__Test__Node(node_id=Random_Guid(), name='name')
        age_node    = Schema__Test__Node(node_id=Random_Guid(), name='age'  )
        value_node  = Schema__Test__Node(node_id=Random_Guid(), value=30    )

        # Add nodes to graph
        graph.nodes[user_node.node_id  ] = user_node
        graph.nodes[name_node.node_id  ] = name_node
        graph.nodes[age_node.node_id   ] = age_node
        graph.nodes[value_node.node_id ] = value_node

        # Create edges
        name_edge = Schema__MGraph__Edge(from_node_id=user_node.node_id,
                                        to_node_id   =name_node.node_id   )
        value_edge = Schema__MGraph__Edge(from_node_id=name_node.node_id,
                                         to_node_id   =value_node.node_id )

        graph.edges[name_edge.edge_config.edge_id  ] = name_edge
        graph.edges[value_edge.edge_config.edge_id ] = value_edge

        # Add nodes and edges to index
        index.add_node(user_node  )
        index.add_node(name_node  )
        index.add_node(age_node   )
        index.add_node(value_node )
        index.add_edge(name_edge  )
        index.add_edge(value_edge )

        return graph, index

class test_Graph__Query(TestCase):

    @classmethod
    def setUpClass(cls):
        pytest.skip("implement once MGraph__Simple is working")

    def setUp(self):                                                                # Initialize test data
        self.graph, self.index = Graph__Query__Test.create_test_graph()
        self.query = Graph__Query(self.index)

    def test_by_type(self):                                                         # Test type-based filtering
        result = self.query.by_type(Schema__Test__Node)
        self.assertTrue(bool(result))
        self.assertIsNotNone(result.value())

    def test_with_attribute(self):                                                  # Test attribute-based filtering
        result = self.query.with_attribute('value', 'john')
        self.assertTrue(bool(result))
        self.assertEqual(result.value(), 'john')

    def test_traverse_properties(self):                                             # Test property traversal
        result = (self.query
                    .by_type(Schema__Test__Node)
                    .name
                    .value()
                 )
        self.assertEqual(result, 30)

    def test_collect(self):                                                         # Test collect method
        result = (self.query
                    .by_type(Schema__Test__Node)
                    .name
                    .collect()
                 )
        self.assertEqual(result, ['age'])

    def test_empty_query(self):                                                     # Test empty query behavior
        result = self.query.with_attribute('non_existent', 'value')
        self.assertFalse(bool(result))
        self.assertIsNone(result.value())

    def test_chained_query(self):                                                   # Test multiple query methods
        result = (self.query
                    .by_type(Schema__Test__Node)
                    .name
                 )
        self.assertTrue(bool(result))

        # Test node truth value
        self.assertTrue(result)
        self.assertFalse(self.query.with_attribute('non_existent', 'value'))

    def test_callable_query(self):                                                  # Test callable query method
        result = (self.query
                    .by_type(Schema__Test__Node)
                    .name
                 )()
        self.assertEqual(result, 'age')