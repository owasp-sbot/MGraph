import pytest
from datetime                                                                               import datetime, UTC
from unittest                                                                               import TestCase
from mgraph_db.mgraph.actions.MGraph__Index                                                 import MGraph__Index
from mgraph_db.providers.time_series.MGraph__Time_Series                                    import MGraph__Time_Series
from mgraph_db.providers.time_series.actions.MGraph__Time_Point__Builder                    import MGraph__Time_Point__Builder
from mgraph_db.providers.time_series.actions.MGraph__Time_Point__Create                     import MGraph__Time_Point__Create
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Time_Point__Created__Objects   import Schema__MGraph__Time_Point__Created__Objects
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Time_Series__Edges             import Schema__MGraph__Time_Series__Edge__Year, Schema__MGraph__Time_Series__Edge__Second
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Value__UTC_Offset        import Schema__MGraph__Node__Value__UTC_Offset
from osbot_utils.utils.Env import load_dotenv


class test_MGraph__Time_Point__Create(TestCase):

    @classmethod
    def setUpClass(cls):
        pytest.skip("complete implemtation and fix tests")
        load_dotenv()
        cls.screenshot_create = True
        cls.screenshot_file   = './time-point-create.png'
        cls.screenshot_delete = False

    def setUp(self):
        self.mgraph            = MGraph__Time_Series()                                         # Setup fresh graph for each test
        self.time_point_create = MGraph__Time_Point__Create(mgraph_edit  = self.mgraph.edit(),
                                                           mgraph_index  = MGraph__Index())
        self.builder          = MGraph__Time_Point__Builder()

    def tearDown(self):
        if self.screenshot_create:
            with self.mgraph.screenshot(target_file=self.screenshot_file) as screenshot:
                with screenshot.export().export_dot() as _:
                    _.show_node__value()
                    _.set_edge_to_node__type_fill_color(Schema__MGraph__Time_Series__Edge__Second, 'azure')
                with screenshot as _:
                    _.save_to(self.screenshot_file)
                    _.dot()

    def test_create_simple_time_point(self):                                                  # Test basic creation
        date_time     = datetime(2025, 2, 10, 12, 30, tzinfo=UTC)
        date_time_str = "Mon, 10 Feb 2025 12:30:00 +0000"
        create_data  = self.builder.from_datetime(date_time)
        time_objects = self.time_point_create.execute(create_data)

        assert type(time_objects) is Schema__MGraph__Time_Point__Created__Objects

        with self.mgraph.data() as data:                                                      # Verify node creation
            time_point = data.node(time_objects.time_point_id)
            assert time_point.node_data.value == date_time_str

            for edge_id in time_objects.component_edges.values():                              # Verify edge creation
                assert data.edge(edge_id) is not None

            for node_id in time_objects.value_nodes.values():                                  # Verify value nodes
                assert data.node(node_id) is not None

    def test_value_reuse(self):                                                               # Test value node reuse
        test_time = datetime(2025, 2, 10, 12, 30, tzinfo=UTC)

        create_data_1  = self.builder.from_datetime(test_time)                                # Create first time point
        time_objects_1 = self.time_point_create.execute(create_data_1)

        create_data_2  = self.builder.from_datetime(test_time)                                # Create second time point
        time_objects_2 = self.time_point_create.execute(create_data_2)

        year_edge_type = Schema__MGraph__Time_Series__Edge__Year                              # Check year value reuse
        assert time_objects_1.value_nodes[year_edge_type] == time_objects_2.value_nodes[year_edge_type]

    def test_timezone_handling(self):                                                         # Test timezone components
        test_time   = datetime(2025, 2, 10, 12, 30, tzinfo=UTC)
        create_data = self.builder.from_datetime(test_time)

        time_objects = self.time_point_create.execute(create_data)
        assert time_objects.timezone_id is not None
        assert time_objects.timezone_edge is not None

        with self.mgraph.data() as data:                                                      # Verify timezone node
            timezone_node = data.node(time_objects.timezone_id)
            assert timezone_node.node_data.value == "UTC"

    def test_partial_time_point(self):                                                        # Test partial time components
        create_data = self.builder.from_components(year=2025, month=2)                        # Only year and month
        time_objects = self.time_point_create.execute(create_data)

        with self.mgraph.data() as data:
            created_edges = [data.edge(edge_id) for edge_id in time_objects.component_edges.values()]
            assert len(created_edges) == 2                                                     # Should only have year and month edges

    def test_utc_offset_creation(self):                                                       # Test UTC offset handling
        test_time = datetime(2025, 2, 10, 12, 30, tzinfo=UTC)
        create_data = self.builder.from_datetime(test_time)

        time_objects = self.time_point_create.execute(create_data)

        with self.mgraph.data() as data:
            with data.index() as index:                                                        # Verify UTC offset node
                offset_nodes = index.get_nodes_by_type(Schema__MGraph__Node__Value__UTC_Offset)
                assert len(offset_nodes) > 0

                offset_node = data.node(next(iter(offset_nodes)))
                assert offset_node.node_data.value == 0                                        # UTC should have offset 0

    def test_index_updates(self):                                                             # Test index maintenance
        test_time   = datetime(2025, 2, 10, 12, 30, tzinfo=UTC)
        create_data = self.builder.from_datetime(test_time)

        self.time_point_create.execute(create_data)                                           # Create time point

        index = self.time_point_create.mgraph_index

        assert len(index.nodes_by_type()) > 0                                                 # Verify index has been updated
        assert len(index.nodes_by_field()) > 0
        assert len(index.edges_by_type()) > 0

    def test_error_cases(self):                                                               # Test error handling
        with self.assertRaises(Exception):                                                    # Invalid create data
            self.time_point_create.execute(None)

        create_data = self.builder.from_components()                                          # Empty create data
        time_objects = self.time_point_create.execute(create_data)
        assert len(time_objects.component_edges) == 0                                         # Should create time point but no components

    def test_execution_idempotency(self):                                                     # Test idempotent behavior
        test_time = datetime(2025, 2, 10, 12, 30, tzinfo=UTC)
        create_data = self.builder.from_datetime(test_time)

        objects_1 = self.time_point_create.execute(create_data)                               # Execute twice
        objects_2 = self.time_point_create.execute(create_data)

        assert objects_1.time_point_id != objects_2.time_point_id                             # Should create new time point
        assert objects_1.value_nodes == objects_2.value_nodes                                 # But reuse value nodes