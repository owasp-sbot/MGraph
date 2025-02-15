from unittest                                                           import TestCase
from mgraph_db.mgraph.MGraph                                            import MGraph
from mgraph_db.mgraph.actions.MGraph__Values                            import MGraph__Values
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                      import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.values.Schema__MGraph__Node__Value__Int   import Schema__MGraph__Node__Value__Int
from mgraph_db.mgraph.schemas.values.Schema__MGraph__Node__Value__Str   import Schema__MGraph__Node__Value__Str
from osbot_utils.utils.Env import load_dotenv


class test_MGraph__Values(TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.screenshot_create = True  # set to true to create a screenshot per test
        cls.screenshot_file = './mgraph-values.png'
        cls.screenshot_delete = False

    def setUp(self):
        self.mgraph = MGraph()                                                                         # Create fresh graph for each test
        self.values = MGraph__Values(mgraph_edit=self.mgraph.edit())

    def tearDown(self):
        if self.screenshot_create:
            with self.mgraph.screenshot(target_file=self.screenshot_file) as screenshot:
                with screenshot.export().export_dot() as _:
                    _.show_node__value()
                    #_.show_edge__ids()
                with screenshot as _:
                    _.save_to(self.screenshot_file)
                    _.dot()

    def test_get_or_create(self):                                                                       # Test direct node creation
        value_node_1 = self.values.get_or_create(42, Schema__MGraph__Node__Value__Int)                  # Create int node
        value_node_2 = self.values.get_or_create(42, Schema__MGraph__Node__Value__Int)                  # Get same node

        assert value_node_1.node_id         == value_node_2.node_id                                     # Verify reuse
        assert value_node_1.node_data.value == 42                                                       # Verify value

        self.mgraph.index().print__index_data()

        str_node_1 = self.values.get_or_create("test", Schema__MGraph__Node__Value__Str)                # Test with string
        str_node_2 = self.values.get_or_create("test", Schema__MGraph__Node__Value__Str)

        assert str_node_1.node_id         == str_node_2.node_id
        assert str_node_1.node_data.value == "test"

    def test_get_or_create_value(self):                                                               # Test value creation with edge
        class Test_Edge(Schema__MGraph__Edge): pass                                                   # Define test edge type

        with self.mgraph.edit() as _:
            root_node = _.new_node()                                                                  # Create root node

            value_node_1, edge_1 = self.values.get_or_create_value(42, Test_Edge, root_node)         # Create value and edge
            value_node_2, edge_2 = self.values.get_or_create_value(42, Test_Edge, root_node)         # Should reuse value node

            assert value_node_1.node_id == value_node_2.node_id                                      # Same value node
            assert edge_1.edge_id != edge_2.edge_id                                                  # Different edges
            assert value_node_1.node_data.value == 42                                                # Correct value

    def test_type_specific_helpers(self):                                                            # Test helper methods
        class Test_Edge(Schema__MGraph__Edge): pass

        with self.mgraph.edit() as _:
            root_node = _.new_node()

            int_node, _ = self.values.get_or_create_int_value(42, Test_Edge, root_node)              # Test int helper
            assert int_node.node_data.value == 42
            assert type(int_node.node_data.value) is int

            str_node, _ = self.values.get_or_create_str_value("test", Test_Edge, root_node)          # Test str helper
            assert str_node.node_data.value == "test"
            assert type(str_node.node_data.value) is str

    def test_get_linked_value(self):                                                                 # Test value retrieval
        class Test_Edge(Schema__MGraph__Edge): pass

        with self.mgraph.edit() as _:
            root_node = _.new_node()
            value_node, _ = self.values.get_or_create_value("test", Test_Edge, root_node)

            linked_node = self.values.get_linked_value(root_node, Test_Edge)                         # Get value through edge
            assert linked_node.node_id == value_node.node_id
            assert linked_node.node_data.value == "test"

    def test_invalid_value_type(self):                                                              # Test error handling
        class Test_Edge(Schema__MGraph__Edge): pass

        with self.mgraph.edit() as _:
            root_node = _.new_node()
            with self.assertRaises(ValueError):                                                      # Should reject lists
                self.values.get_or_create_value([1,2,3], Test_Edge, root_node)

    def test_multiple_edges_to_value(self):                                                         # Test multiple connections
        class Edge_1(Schema__MGraph__Edge): pass
        class Edge_2(Schema__MGraph__Edge): pass

        with self.mgraph.edit() as _:
            root_1 = _.new_node()
            root_2 = _.new_node()

            value_1, edge_1 = self.values.get_or_create_value(42, Edge_1, root_1)                   # Create with first edge
            value_2, edge_2 = self.values.get_or_create_value(42, Edge_2, root_2)                   # Create with second edge

            assert value_1.node_id == value_2.node_id                                               # Same value node
            assert edge_1.edge_id != edge_2.edge_id                                                 # Different edges

            value_1_linked = self.values.get_linked_value(root_1, Edge_1)                          # Test both links work
            value_2_linked = self.values.get_linked_value(root_2, Edge_2)

            assert value_1_linked.node_id == value_2_linked.node_id                                # Both lead to same value
            assert value_1_linked.node_data.value == 42

    def test_get_value_type(self):                                                                 # Test type resolution
        assert self.values.get_value_type(42) == Schema__MGraph__Node__Value__Int                 # Integer type
        assert self.values.get_value_type("test") == Schema__MGraph__Node__Value__Str             # String type
        assert self.values.get_value_type([1,2,3]) is None                                        # Unsupported type