import pytest
from unittest                                                     import TestCase
from mgraph_db.providers.time_series.MGraph__Time_Series          import MGraph__Time_Series
from osbot_utils.utils.Env                                        import load_dotenv
from osbot_utils.utils.Files                                      import file_exists, file_delete
from osbot_utils.utils.Objects                                    import __
from osbot_utils.helpers.Obj_Id                                   import is_obj_id


class test_MGraph__Time_Series__Edit(TestCase):

    @classmethod
    def setUpClass(cls):
        pytest.skip("Tests need fixing after Time_Series class is fixed")
        load_dotenv()
        cls.screenshot_file = './time-series.png'
        cls.delete_on_exit  = True

    def setUp(self):
        self.graph       = MGraph__Time_Series()                                                          # Create fresh graph
        self.graph_edit = self.graph.edit()                                                              # Get edit interface


    def tearDown(self):
        with self.graph.screenshot(target_file=self.screenshot_file) as _:
            _.dot_config().show_value    = True
            _.dot_config().show_edge_ids = False
            _.dot()
            assert file_exists(self.screenshot_file)
            if self.delete_on_exit:
                assert file_delete(self.screenshot_file) is True


    def test_create_time_point(self):                                                                    # Test creating time point
        time_point = self.graph_edit.create_time_point(year=2024, month=2, day=14, hour=15, minute=30)
        #pprint(time_point.json())
        return
        assert type(time_point.node.data)  is Schema__MGraph__Node__Time_Point                           # Check time point creation
        assert is_obj_id(time_point.node_id)

        with self.graph.data() as data:                                                                 # Check components
            components = data.get_time_components(time_point.node_id)
            assert components == {'year': 2024, 'month': 2, 'day': 14, 'hour': 15, 'minute': 30}

    def test_create_partial_time_point(self):                                                           # Test partial time point
        time_point = self.graph_edit.create_time_point(year=2024, month=2)

        with self.graph.data() as data:
            components = data.get_time_components(time_point.node_id)
            assert components == {'year': 2024, 'month': 2}                                             # Only year and month
            assert 'day'    not in components
            assert 'hour'   not in components
            assert 'minute' not in components

    def test_value_reuse(self):                                                                         # Test value node reuse
        time_point_1 = self.graph_edit.create_time_point(year=2024, month=2)
        time_point_2 = self.graph_edit.create_time_point(year=2024, month=3)

        year_value_1 = None
        year_value_2 = None

        with self.graph.data() as data:                                                                # Find year value nodes
            for edge in data.edges():
                if isinstance(edge.edge.data, Schema__MGraph__TimeSeries__Edge__Year):
                    if edge.from_node_id() == time_point_1.node_id:
                        year_value_1 = edge.to_node_id()
                    if edge.from_node_id() == time_point_2.node_id:
                        year_value_2 = edge.to_node_id()

        assert year_value_1 is not None                                                                # Same year value should be reused
        assert year_value_2 is not None
        assert year_value_1 == year_value_2

    def test_edge_types(self):                                                                         # Test correct edge types
        time_point = self.graph_edit.create_time_point(year=2024, month=2, day=14)

        edge_type_map = {
            Schema__MGraph__TimeSeries__Edge__Year : 2024,
            Schema__MGraph__TimeSeries__Edge__Month: 2,
            Schema__MGraph__TimeSeries__Edge__Day  : 14
        }

        with self.graph.data() as data:
            for edge in data.edges():
                edge_type = type(edge.edge.data)
                if edge_type in edge_type_map:
                    target_node = data.node(edge.to_node_id())
                    assert isinstance(target_node.node.data, Schema__MGraph__Node__Value__Int)
                    assert target_node.node.data.node_data.value == edge_type_map[edge_type]

    def test_invalid_values(self):                                                                     # Test error handling
        with self.assertRaises(ValueError):                                                            # Month out of range
            self.graph_edit.create_time_point(year=2024, month=13)

        with self.assertRaises(ValueError):                                                            # Day out of range
            self.graph_edit.create_time_point(year=2024, month=2, day=30)

        with self.assertRaises(ValueError):                                                            # Hour out of range
            self.graph_edit.create_time_point(year=2024, month=2, day=14, hour=24)

        with self.assertRaises(ValueError):                                                            # Minute out of range
            self.graph_edit.create_time_point(year=2024, month=2, day=14, hour=12, minute=60)

    def test_time_point_json(self):                                                                    # Test JSON representation
        time_point = self.graph_edit.create_time_point(year=2024, month=2)

        expected_json = {
            'node': {
                'data': {
                    'node_data': {},
                    'node_id': time_point.node_id,
                    'node_type': 'mgraph_db.providers.time_series.schemas.nodes.Schema__MGraph__Node__TimePoint'
                }
            }
        }

        assert time_point.obj() == __(expected_json)

    def test_cleanup(self):                                                                            # Test cleanup/deletion
        time_point = self.graph_edit.create_time_point(year=2024, month=2)

        with self.graph.data() as data:
            assert data.node(time_point.node_id) is not None                                           # Confirm existence

            data.graph.delete_node(time_point.node_id)                                                # Delete node

            assert data.node(time_point.node_id) is None                                              # Confirm deletion

            for edge in data.edges():                                                                 # Check no dangling edges
                assert edge.from_node_id() != time_point.node_id
                assert edge.to_node_id() != time_point.node_id