from unittest                                                   import TestCase
from mgraph_db.mgraph.MGraph                                    import MGraph
from mgraph_db.mgraph.domain.Domain__MGraph__Node import Domain__MGraph__Node
from mgraph_db.mgraph.models.Model__MGraph__Graph import Model__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge              import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Node              import Schema__MGraph__Node
from mgraph_db.mgraph.actions.MGraph__Diff                      import MGraph__Diff
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data        import Schema__MGraph__Node__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value       import Schema__MGraph__Node__Value
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value__Data import Schema__MGraph__Node__Value__Data
from osbot_utils.utils.Objects import __, type_full_name

from osbot_utils.utils.Dev import pprint

class test_MGraph__Diff(TestCase):
    @classmethod
    def setUpClass(cls):
        import pytest
        pytest.skip("fix remaining tests")

    def setUp(self):
        self.graph_a = MGraph()
        self.graph_b = MGraph()

    def test_compare_identical_graphs(self):
        diff  = MGraph__Diff(graph_a=self.graph_a.graph, graph_b=self.graph_b.graph)
        stats = diff.compare()

        # Empty graphs should have no differences
        assert len(stats.nodes_added)       == 0
        assert len(stats.nodes_removed)     == 0
        assert len(stats.nodes_modified)    == 0
        assert len(stats.edges_added)       == 0
        assert len(stats.edges_removed)     == 0
        assert len(stats.edges_modified)    == 0
        assert stats.nodes_count_diff       == 0
        assert stats.edges_count_diff       == 0

    def test_compare_different_nodes(self):

        with self.graph_a.edit() as edit_a:                 # Add a node to graph A
            node_a = edit_a.new_node()

        with self.graph_b.edit() as edit_b:                 # Add a different node to graph B
            node_b = edit_b.new_node()

        diff = MGraph__Diff(graph_a=self.graph_a.graph, graph_b=self.graph_b.graph)
        stats = diff.compare()

        assert node_b.node_id in stats.nodes_added
        assert node_a.node_id in stats.nodes_removed
        assert stats.nodes_count_diff == 0  # Same number of nodes

        assert stats.obj() == __(nodes_added      = [node_b.node_id],
                                 nodes_removed    = [node_a.node_id],
                                 nodes_modified   = [],
                                 edges_added      = [],
                                 edges_removed    = [],
                                 edges_modified   = [],
                                 nodes_count_diff = 0,
                                 edges_count_diff = 0)

    def test_compare_modified_node(self):
        class NodeA(Schema__MGraph__Node): pass                                 # Create custom node types
        class NodeB(Schema__MGraph__Node): pass


        with self.graph_a.edit() as edit_a:                                             # Add same node to both graphs but with different types
            node_a = edit_a.new_node(node_type=NodeA)

        with self.graph_b.edit() as edit_b:
            node_b        = edit_b.new_node(node_type=NodeB, node_id=node_a.node_id)    # Force same ID for testing

        diff  = MGraph__Diff(graph_a=self.graph_a.graph, graph_b=self.graph_b.graph)
        stats = diff.compare()

        assert node_b.node_id == node_a.node_id
        assert stats.obj() == __(nodes_added      = [],
                                 nodes_removed    = [],
                                 nodes_modified   = [node_a.node_id],
                                 edges_added      = [],
                                 edges_removed    = [],
                                 edges_modified   = [],
                                 nodes_count_diff = 0 ,
                                 edges_count_diff = 0 )

        assert node_a.node_id in stats.nodes_modified

        changes = diff.compare_node_data(node_a.node_id)                # Check specific differences
        assert changes['type']['from'] == 'NodeA'
        assert changes['type']['to'  ] == 'NodeB'

        assert changes == {'data': {'from': {}     , 'to': {}      },
                           'type': {'from': 'NodeA', 'to': 'NodeB'}}

    def test_compare_edges(self):
        class CustomEdge(Schema__MGraph__Edge): pass                        # Create custom edge type

        # Setup graph A
        with self.graph_a.edit() as edit_a:
            node_a1 = edit_a.new_node()
            node_a2 = edit_a.new_node()
            edge_a  = edit_a.new_edge(from_node_id = node_a1.node_id        ,
                                      to_node_id   = node_a2.node_id        ,
                                      edge_type    = Schema__MGraph__Edge   )


        with self.graph_b.edit() as edit_b:                                     # Setup graph B with same nodes but different edge
            node_b1 = edit_b.new_node(node_id      = node_a1.node_id )
            node_b2 = edit_b.new_node(node_id      = node_a2.node_id )
            edge_b  = edit_b.new_edge(from_node_id = node_b1.node_id ,
                                      to_node_id   = node_b2.node_id ,
                                      edge_type    = CustomEdge      )

        diff  = MGraph__Diff(graph_a=self.graph_a.graph, graph_b=self.graph_b.graph)
        stats = diff.compare()

        assert edge_a.edge_id in stats.edges_removed
        assert edge_b.edge_id in stats.edges_added
        assert stats.obj() == __(nodes_added      = [],
                                 nodes_removed    = [],
                                 nodes_modified   = sorted([ node_a1.node_id, node_a2.node_id]),
                                 edges_added      = [ edge_b.edge_id],
                                 edges_removed    = [ edge_a.edge_id],
                                 edges_modified   = [],
                                 nodes_count_diff = 0,
                                 edges_count_diff = 0)


    def test_node_data_changes(self):
        class CustomNodeData(Schema__MGraph__Node__Data):                                    # Create custom node types with data
            field_1: str
            field_2: int

        class CustomNode(Schema__MGraph__Node):
            node_data: CustomNodeData

        with self.graph_a.edit() as edit_a:                                                 # Add node with data to both graphs
            node_a = edit_a.new_node(node_type = CustomNode    ,
                                    field_1   = "original"    ,
                                    field_2   = 42           )

        with self.graph_b.edit() as edit_b:
            node_b = edit_b.new_node(node_type = CustomNode       ,                         # Changed field_1, same field_2
                                     node_id   = node_a.node_id   ,
                                     field_1   = "modified"       ,
                                     field_2   = 42              )

        diff    = MGraph__Diff(graph_a=self.graph_a.graph, graph_b=self.graph_b.graph)
        stats   = diff.compare()
        changes = diff.compare_node_data(node_a.node_id)

        assert node_a.node_id in stats.nodes_modified
        assert changes        == {'data': {'from': {'field_1': "original", 'field_2': 42},
                                           'to'  : {'field_1': "modified", 'field_2': 42}}}

    def test_value_node_changes(self):
        with self.graph_a.edit() as edit_a:                                                  # Create value nodes with different values
            value_data_a = Schema__MGraph__Node__Value__Data(value      = "original_value"           ,
                                                             value_type = str                        )
            node_a       = edit_a.new_node                  (node_type  = Schema__MGraph__Node__Value,
                                                             node_data  = value_data_a               )
            node_a_id    = node_a.node_id

        assert type(node_a          ) is Domain__MGraph__Node
        assert type(node_a.node_data) is Schema__MGraph__Node__Value__Data
        assert node_a.node_type       is Schema__MGraph__Node__Value
        assert type(node_a.graph)     is Model__MGraph__Graph
        assert node_a.graph           == self.graph_a.graph.model
        assert node_a.graph           == edit_a.graph.model
        assert node_a.node.obj()      == __(data=__(node_data = __(value_type = 'builtins.str'  ,
                                                                   value      = 'original_value',
                                                                   key        = ''              ),
                                                    node_id   = node_a_id,
                                                    node_type = type_full_name(Schema__MGraph__Node__Value)))


        with self.graph_b.edit() as edit_b:
            value_data_b = Schema__MGraph__Node__Value__Data(value      = "new_value"                ,
                                                             value_type = str                        )
            node_b       = edit_b.new_node                  (node_type  = Schema__MGraph__Node__Value,
                                                             node_id    = node_a.node_id             ,
                                                             node_data  = value_data_b               )
            node_b_id    = node_b.node_id

        diff    = MGraph__Diff(graph_a=self.graph_a.graph, graph_b=self.graph_b.graph)
        stats   = diff.compare()
        assert node_a_id   == node_b_id
        assert stats.obj() == __(nodes_added      = [],
                                 nodes_removed    = [],
                                 nodes_modified   = [node_a_id],
                                 edges_added      = [],
                                 edges_removed    = [],
                                 edges_modified   = [],
                                 nodes_count_diff = 0,
                                 edges_count_diff = 0)

        changes = diff.compare_node_data(node_a.node_id)
        assert changes             != {}                                # BUG (and the ones below)
        assert node_a.node_id in stats.nodes_modified
        assert changes            == {'data': {'from': {'key': '', 'value': 'original_value', 'value_type': 'builtins.str'},
                                               'to'  : {'key': '', 'value': 'new_value'     , 'value_type': 'builtins.str'}}}

    def test_edge_connection_changes(self):
        with self.graph_a.edit() as edit_a:
            node_a1 = edit_a.new_node()
            node_a2 = edit_a.new_node()
            node_a3 = edit_a.new_node()
            edge_a  = edit_a.new_edge(from_node_id = node_a1.node_id,
                                     to_node_id   = node_a2.node_id)

        with self.graph_b.edit() as edit_b:                                                  # Create nodes with same IDs
            node_b1 = edit_b.new_node(node_id = node_a1.node_id)
            node_b2 = edit_b.new_node(node_id = node_a2.node_id)
            node_b3 = edit_b.new_node(node_id = node_a3.node_id)

            edge_b  = edit_b.new_edge(edge_id    = edge_a.edge_id    ,                      # Create edge with same ID but different target
                                      from_node_id = node_b1.node_id   ,
                                      to_node_id   = node_b3.node_id   )

        diff    = MGraph__Diff(graph_a=self.graph_a.graph, graph_b=self.graph_b.graph)
        stats   = diff.compare()
        changes = diff.compare_edge_data(edge_a.edge_id)

        return
        assert edge_a.edge_id in stats.edges_modified
        assert changes == {'to_node': {'from': str(node_a2.node_id),
                                      'to'  : str(node_b3.node_id)}}

    def test_edge_type_changes(self):
        class EdgeTypeA(Schema__MGraph__Edge): pass                                         # Create custom edge types
        class EdgeTypeB(Schema__MGraph__Edge): pass

        with self.graph_a.edit() as edit_a:
            node_a1 = edit_a.new_node()
            node_a2 = edit_a.new_node()
            edge_a  = edit_a.new_edge(from_node_id = node_a1.node_id,
                                     to_node_id   = node_a2.node_id,
                                     edge_type    = EdgeTypeA     )

        with self.graph_b.edit() as edit_b:                                                  # Create nodes with same IDs
            node_b1 = edit_b.new_node(node_id = node_a1.node_id)
            node_b2 = edit_b.new_node(node_id = node_a2.node_id)

            edge_b  = edit_b.new_edge(edge_id     = edge_a.edge_id   ,                      # Create edge with same ID but different type
                                     from_node_id = node_b1.node_id  ,
                                     to_node_id   = node_b2.node_id  ,
                                     edge_type    = EdgeTypeB       )

        diff    = MGraph__Diff(graph_a=self.graph_a.graph, graph_b=self.graph_b.graph)
        stats   = diff.compare()
        changes = diff.compare_edge_data(edge_a.edge_id)

        assert edge_a.edge_id in stats.edges_modified
        assert changes == {'type': {'from': 'EdgeTypeA',
                                   'to'  : 'EdgeTypeB'}}

    def test_complex_graph_changes(self):
        class CustomNode(Schema__MGraph__Node): pass                                         # Create custom types
        class CustomEdge(Schema__MGraph__Edge): pass

        with self.graph_a.edit() as edit_a:                                                  # Setup graph A
            node_a1 = edit_a.new_node()
            node_a2 = edit_a.new_node(node_type = CustomNode)
            node_a3 = edit_a.new_node()

            edge_a1 = edit_a.new_edge(from_node_id = node_a1.node_id,
                                     to_node_id   = node_a2.node_id)
            edge_a2 = edit_a.new_edge(from_node_id = node_a2.node_id,
                                     to_node_id   = node_a3.node_id,
                                     edge_type    = CustomEdge    )

        with self.graph_b.edit() as edit_b:                                                  # Setup graph B with various changes
            node_b1 = edit_b.new_node(node_id = node_a1.node_id)                            # Keep node_1
            node_b2 = edit_b.new_node(node_id = node_a2.node_id)                            # Modify node_2
            node_b4 = edit_b.new_node()                                                      # Add node_4 (node_3 removed)

            edge_b1 = edit_b.new_edge(edge_id     = edge_a1.edge_id   ,                     # Modify edge_1
                                     from_node_id = node_b1.node_id   ,
                                     to_node_id   = node_b2.node_id   ,
                                     edge_type    = CustomEdge       )
            edge_b3 = edit_b.new_edge(from_node_id = node_b2.node_id,                       # Add edge_3 (edge_2 removed)
                                     to_node_id   = node_b4.node_id)

        diff  = MGraph__Diff(graph_a=self.graph_a.graph, graph_b=self.graph_b.graph)
        stats = diff.compare()

        assert stats.obj() == __(nodes_added      = [node_b4.node_id]   ,                   # Check all changes
                                nodes_removed     = [node_a3.node_id]   ,
                                nodes_modified    = [node_a2.node_id]   ,
                                edges_added       = [edge_b3.edge_id]   ,
                                edges_removed     = [edge_a2.edge_id]   ,
                                edges_modified    = [edge_a1.edge_id]   ,
                                nodes_count_diff  = 0                   ,                     # Same total nodes and edges
                                edges_count_diff  = 0                   )

    def test_empty_and_null_cases(self):
        diff = MGraph__Diff(graph_a=self.graph_a.graph, graph_b=self.graph_b.graph)

        assert diff.compare_node_data(None) == {}                                           # Test comparing non-existent node
        assert diff.compare_edge_data(None) == {}                                           # Test comparing non-existent edge

        with self.graph_b.edit() as edit_b:                                                 # Compare empty to non-empty graph
            node_b = edit_b.new_node()
            edge_b = edit_b.new_edge(from_node_id = node_b.node_id,
                                    to_node_id   = node_b.node_id)

        stats = diff.compare()
        assert stats.obj() == __(nodes_added      = [node_b.node_id]   ,
                                nodes_removed     = []                  ,
                                nodes_modified    = []                  ,
                                edges_added       = [edge_b.edge_id]    ,
                                edges_removed     = []                  ,
                                edges_modified    = []                  ,
                                nodes_count_diff  = 1                   ,
                                edges_count_diff  = 1                   )