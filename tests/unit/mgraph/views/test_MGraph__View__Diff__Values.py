from unittest                                                import TestCase
from mgraph_db.mgraph.schemas.Schema__MGraph__Diff__Values   import Schema__MGraph__Diff__Values
from mgraph_db.mgraph.views.MGraph__View__Diff__Values       import (MGraph__View__Diff__Values,
                                                                     Edge__Diff__Added,
                                                                     Edge__Diff__Removed,
                                                                     Edge__Diff__Type)

class test_MGraph__View__Diff__Values(TestCase):

    def setUp(self):                                                                         # Setup for each test
        self.diff = Schema__MGraph__Diff__Values()
        self.view = MGraph__View__Diff__Values(diff=self.diff)

    # def tearDown(self):                                                                     # Create screenshot after each test
    #     load_dotenv()
    #     screenshot_file = type(self).__name__  + '.png'
    #     with self.view.create_mgraph_screenshot() as _:
    #         _.save_to(screenshot_file)
    #         _.dot()

    def test_init(self):                                                                    # Test initialization
        assert type(self.view.diff)   is Schema__MGraph__Diff__Values
        assert self.view.mgraph       is not None

    def test_create_graph__empty_diff(self):                                               # Test with empty diff
        graph = self.view.create_graph()
        with graph.data() as _:
            assert len(_.nodes_ids()) == 3                                                  # Center + Added + Removed nodes
            assert len(_.edges_ids()) == 2                                                  # Two type edges to sections

    def test_create_graph__with_values(self):                                              # Test with actual values
        self.diff.added_values[str]   = {"value1", "value2"}                               # Add some test data
        self.diff.removed_values[int] = {"42", "123"}

        graph = self.view.create_graph()
        with graph.data() as _:
            assert len(_.nodes_ids()) == 9                                                  # Center + Added + Removed + 2 types + 4 values
            assert len(_.edges_ids()) == 8                                                  # 2 section edges + 2 type edges + 4 value edges

            # Verify edge types present
            edge_types = set()
            for edge in _.edges():
                edge_type = edge.edge.data.edge_type
                edge_types.add(edge_type)

            assert Edge__Diff__Type    in edge_types                                        # Should have all three edge types
            assert Edge__Diff__Added   in edge_types
            assert Edge__Diff__Removed in edge_types

    def test_create_graph__multiple_types(self):                                           # Test with multiple types
        self.diff.added_values   = { str  : {"added_str1", "added_str2"},
                                     int  : {"4"   },
                                     float: {"3.14"}}
        self.diff.removed_values = { str : {"removed_str1"}, bool: {"True"} }

        graph = self.view.create_graph()
        with graph.data() as _:
            total_values    = 5                                                             # 4 added + 1 removed values
            total_types     = 5                                                             # str, int, float, bool, str(removed)
            section_nodes   = 3                                                             # Center + Added + Removed
            expected_nodes  = section_nodes + total_types + total_values + 1
            type_edges      = 2                                                             # From center to sections
            value_edges     = total_types + total_values                  +1                # Type connections + value connections
            expected_edges  = type_edges + value_edges

            assert len(_.nodes_ids()) == expected_nodes
            assert len(_.edges_ids()) == expected_edges

    def test_create_mgraph_screenshot(self):                                                # Test screenshot configuration
        self.diff.added_values[str] = {"test1", "test2"}                                   # Add some test data
        graph = self.view.create_graph()

        with self.view.create_mgraph_screenshot() as screenshot:
            with screenshot.export().export_dot() as dot:
                dot_code = dot.process_graph()

                # Verify key visualization settings
                assert 'layout="dot"'             in dot_code                                 # Layout engine
                assert 'rankdir="LR"'             in dot_code                                 # Direction
                assert 'arrowhead="vee"'          in dot_code                                 # Arrow style
                assert all(color in dot_code for color in                                    # Color scheme present
                          ["#F0FFFF", "#98FB98",  "#E8E8E8"])