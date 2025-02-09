from datetime                                                                            import datetime
from unittest                                                                            import TestCase
from mgraph_db.mgraph.actions.MGraph__Export                                             import MGraph__Export
from mgraph_db.mgraph.actions.MGraph__Index                                              import MGraph__Index
from mgraph_db.mgraph.actions.exporters.dot.MGraph__Export__Dot                          import MGraph__Export__Dot
from mgraph_db.mgraph.domain.Domain__MGraph__Node                                        import Domain__MGraph__Node
from mgraph_db.mgraph.models.Model__MGraph__Node                                         import Model__MGraph__Node
from mgraph_db.providers.time_series.MGraph__Time_Series                                 import MGraph__Time_Series
from mgraph_db.providers.time_series.actions.MGraph__Time_Series__Edit                   import MGraph__Time_Series__Edit
from mgraph_db.providers.time_series.actions.MGraph__Time_Series__Screenshot             import MGraph__Time_Series__Screenshot
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Time_Point            import Schema__MGraph__Node__Time_Point
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Value__Int            import Schema__MGraph__Node__Value__Int
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Value__Int__Data      import Schema__MGraph__Node__Value__Int__Data
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Value__Timezone__Name import Schema__MGraph__Node__Value__Timezone__Name
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Value__UTC_Offset     import Schema__MGraph__Node__Value__UTC_Offset
from mgraph_db.providers.time_series.schemas.Schema__MGraph__TimeSeries__Edges           import (
    Schema__MGraph__Time_Series__Edge__Year  ,
    Schema__MGraph__Time_Series__Edge__Month ,
    Schema__MGraph__Time_Series__Edge__Day   ,
    Schema__MGraph__Time_Series__Edge__Hour  ,
    Schema__MGraph__Time_Series__Edge__Minute,
    Schema__MGraph__Time_Series__Edge__Second)
from osbot_utils.utils.Env                                                               import load_dotenv
from osbot_utils.utils.Files                                                             import file_exists, file_delete
from osbot_utils.utils.Objects                                                           import __, type_full_name
from osbot_utils.helpers.Obj_Id                                                          import is_obj_id


class test_MGraph__Time_Series__Edit(TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.screenshot_create = False
        cls.screenshot_file   = './time-series.png'
        cls.screenshot_delete = False

    def setUp(self):
        self.graph       = MGraph__Time_Series()                                                    # Create fresh graph
        self.graph_edit = self.graph.edit()                                                        # Get edit interface

    def tearDown(self):
        if self.screenshot_create:
            with self.graph.screenshot(target_file=self.screenshot_file) as _:
                assert type(_)                       is MGraph__Time_Series__Screenshot
                assert type(_.export().export_dot()) is MGraph__Export__Dot
                assert _.export_class                is MGraph__Export


                (_.export().export_dot()
                    # Basic node and edge display configuration
                    .show_node__value()
                    #.show_node__type()
                    .show_edge__type()
                    .show_edge__ids()
                    .set_node__font__size(12)                    # Slightly larger font for better readability
                    .set_node__font__name('Arial')
                    .set_edge__font__name('Arial')
                    .set_edge__font__size(11)                    # Slightly larger font for edge labels

                    # Global node styling
                    .set_node__type_fill_color(Schema__MGraph__Node__Time_Point, '#1a365d')
                    .set_node__type_font_color(Schema__MGraph__Node__Time_Point, 'white')
                    .set_node__type_shape     (Schema__MGraph__Node__Time_Point, 'box')
                    .set_node__type_style     (Schema__MGraph__Node__Time_Point, 'rounded')

                    # Time component styling
                    .set_node__type_fill_color(Schema__MGraph__Node__Value__Int, '#D8E6F3')  # Soft blue for time values
                    .set_node__type_shape     (Schema__MGraph__Node__Value__Int, 'ellipse')
                    .set_node__type_font_color(Schema__MGraph__Node__Value__Int, 'darkblue')
                    .set_node__type_font_size (Schema__MGraph__Node__Value__Int, 18)

                    # Timezone styling
                    .set_node__type_fill_color(Schema__MGraph__Node__Value__Timezone__Name, '#B8D0E6')  # Darker blue for timezone
                    .set_node__type_shape     (Schema__MGraph__Node__Value__Timezone__Name, 'box')
                    .set_node__type_style     (Schema__MGraph__Node__Value__Timezone__Name, 'rounded')
                    .set_node__type_font_size (Schema__MGraph__Node__Value__Timezone__Name, 12)

                    # UTC offset styling
                    .set_node__type_fill_color(Schema__MGraph__Node__Value__UTC_Offset, '#E6E6FA')      # Light purple/lavender for offset
                    .set_node__type_shape     (Schema__MGraph__Node__Value__UTC_Offset, 'octagon')
                    .set_node__type_font_size (Schema__MGraph__Node__Value__UTC_Offset, 12)

                    # Edge styling
                    .set_edge__color('#6666FF')                   # Darker gray for edges
                    .set_edge__font__color('#6666FF')
                    .set_edge__type_style(Schema__MGraph__Time_Series__Edge__Year, 'solid')  # Ensure all edges are solid

                    # Graph-level settings
                    .set_graph__rank_dir__tb()                    # Top to bottom layout
                    .set_graph__rank_sep(0.75)                    # Increased vertical spacing
                    .set_graph__node_sep(0.5)                      # Increased horizontal spacing
                )

                _.dot(print_dot_code=True)

                assert file_exists(self.screenshot_file) is True
                if self.screenshot_delete:
                    assert file_delete(self.screenshot_file) is True

    def test_create_time_point(self):
        time_point = self.graph_edit.create_time_point(year=2024, month=2, day=14, hour=15, minute=30)

        assert type(time_point)            is Domain__MGraph__Node
        assert type(time_point.node.data)  is Schema__MGraph__Node__Time_Point
        assert is_obj_id(time_point.node_id)

        with self.graph.data() as data:
            components = self.get_time_components(time_point.node_id, data)
            assert components == {'year': 2024, 'month': 2, 'day': 14, 'hour': 15, 'minute': 30}

    def test_create_time_point__from_datetime(self):
        #test_datetime = datetime(2024, 2, 8, 15, 30)                                         # Create test datetime
        test_datetime       = datetime.now()
        expected_components = { 'year'  : test_datetime.year   ,
                                'month' : test_datetime.month  ,
                                'day'   : test_datetime.day    ,
                                'hour'  : test_datetime.hour   ,
                                'minute': test_datetime.minute ,
                                'second': test_datetime.second }
        time_point = self.graph_edit.create_time_point__from_datetime(test_datetime)          # Create time point from datetime

        assert type(time_point.node.data) is Schema__MGraph__Node__Time_Point               # Verify node type
        assert is_obj_id(time_point.node_id)

        with self.graph.data() as data:                                                     # Verify components match datetime
            components = self.get_time_components(time_point.node_id, data)
            assert components == expected_components

    def test__setUp(self):
        with self.graph_edit as _:
            assert type(_) is MGraph__Time_Series__Edit

    def test_find_int_value(self):
        with self.graph_edit as _:
            assert _.find_int_value(42) is None

            test_value = 42
            value_node = _.new_node(node_type = Schema__MGraph__Node__Value__Int,
                                    value     = test_value)
            value_node_id = value_node.node_id
            assert type(value_node)           is Domain__MGraph__Node
            assert type(value_node.node)      is Model__MGraph__Node
            assert type(value_node.node.data) is Schema__MGraph__Node__Value__Int
            assert type(value_node.node_data) is Schema__MGraph__Node__Value__Int__Data
            assert value_node.node.obj()      == __(data      = __(node_data = __(value=42),
                                                                   node_id   = value_node_id,
                                                                   node_type = type_full_name(Schema__MGraph__Node__Value__Int)))

            _.index().add_node(value_node.node.data)
            assert _.index().index_data.nodes_by_field == {'value': {42: {value_node_id}}}

            found_id = _.find_int_value(test_value)
            assert found_id == value_node.node_id

    def test_create_partial_time_point(self):
        time_point = self.graph_edit.create_time_point(year=2024, month=2)

        with self.graph.data() as data:
            components = self.get_time_components(time_point.node_id, data)
            assert components == {'year': 2024, 'month': 2}
            assert 'day'    not in components
            assert 'hour'   not in components
            assert 'minute' not in components

    def test_value_reuse(self):
        self.graph_edit.create_time_point(year=2024, month=2)
        self.graph_edit.create_time_point(year=2024, month=3)

        with self.graph.data() as data:
            year_edges = [edge for edge in data.edges()
                         if edge.edge.data.edge_type is Schema__MGraph__Time_Series__Edge__Year]

            year_values = {edge.to_node_id() for edge in year_edges}
            assert len(year_values) == 1, "Year value should be reused"

            year_node = data.node(next(iter(year_values)))
            assert year_node.node_data.value == 2024

    def test_edge_types(self):
        self.graph_edit.create_time_point(year=2024, month=2, day=14)

        edge_type_map = {   Schema__MGraph__Time_Series__Edge__Year : 2024  ,
                            Schema__MGraph__Time_Series__Edge__Month: 2     ,
                            Schema__MGraph__Time_Series__Edge__Day  : 14    }

        with self.graph.data() as data:
            for edge in data.edges():
                edge_type = type(edge.edge.data)
                if edge_type in edge_type_map:
                    target_node = data.node(edge.to_node_id())
                    assert isinstance(target_node.node.data, Schema__MGraph__Node__Value__Int)
                    assert target_node.node_data.value == edge_type_map[edge_type]

    def test_cleanup(self):
        time_point = self.graph_edit.create_time_point(year=2024, month=2)

        with self.graph.data() as data:
            assert data.node(time_point.node_id) is not None

            data.graph.delete_node(time_point.node_id)
            assert data.node(time_point.node_id) is None

            for edge in data.edges():
                assert edge.from_node_id() != time_point.node_id
                assert edge.to_node_id() != time_point.node_id

    def get_time_components(self, time_point_id, data):                                     # Helper method to extract time components from a time point using index
        components = {}
        edge_type_to_component = {  Schema__MGraph__Time_Series__Edge__Year  : 'year'  ,
                                    Schema__MGraph__Time_Series__Edge__Month : 'month' ,
                                    Schema__MGraph__Time_Series__Edge__Day   : 'day'   ,
                                    Schema__MGraph__Time_Series__Edge__Hour  : 'hour'  ,
                                    Schema__MGraph__Time_Series__Edge__Minute: 'minute',
                                    Schema__MGraph__Time_Series__Edge__Second: 'second'}

        index = MGraph__Index.from_graph(data.graph)                                                # Create/get index for graph

        outgoing_edges = index.nodes_to_outgoing_edges().get(time_point_id, set())                 # Get all outgoing edges efficiently

        for edge_id in outgoing_edges:                                                             # Process each outgoing edge
            edge = data.edge(edge_id)                                                              # Get edge data
            edge_type = edge.edge.data.edge_type                                                       # Get edge type

            if edge_type in edge_type_to_component:                                                # If it's a time component edge
                value_node = data.node(edge.to_node_id())                                          # Get the value node
                component_name = edge_type_to_component[edge_type]                                  # Get component name
                components[component_name] = value_node.node_data.value                             # Store component value

        return components

    def test_get_or_create_utc_offset(self):
        with self.graph_edit as _:
            offset_node_1 = _.get_or_create__utc_offset(-300)                                       # Test first creation (-5 hours)
            assert isinstance(offset_node_1.node.data, Schema__MGraph__Node__Value__UTC_Offset)
            assert offset_node_1.node_data.value == -300

            offset_node_2 = _.get_or_create__utc_offset(-300)                                       # Test reuse of same offset
            assert offset_node_2.node_id == offset_node_1.node_id                                   # Should get same node

            offset_node_3 = _.get_or_create__utc_offset(60)                                         # Test different offset (+1 hour)
            assert offset_node_3.node_id != offset_node_1.node_id                                   # Should be different node
            assert offset_node_3.node_data.value == 60

            offset_nodes = _.index().get_nodes_by_type(Schema__MGraph__Node__Value__UTC_Offset)     # Verify using index
            assert len(offset_nodes) == 2                                                           # Should have two distinct offset nodes

            matching_nodes = _.index().get_nodes_by_field('value', -300)
            assert offset_node_1.node_id in matching_nodes                                          # Should find original node


    def test_utc_offset_reuse(self):
        # Create two time points with the same UTC offset using valid timezone strings
        point_1 = self.graph_edit.create_time_point__with_tz(year=2024, month=2, day=8, hour=15, minute=30, timezone='Etc/GMT+5')
        point_2 = self.graph_edit.create_time_point__with_tz(year=2024, month=2, day=8, hour=15, minute=30, timezone='America/New_York')

        def get_utc_offset_from_point(point__node_id):
            with self.graph.data() as data:
                with data.index() as _:
                    time_zone__node_id  = _.get_node_connected_to_node__outgoing(point__node_id    , 'Schema__MGraph__Time_Series__Edge__Timezone'  )
                    utc_offset__node_id = _.get_node_connected_to_node__outgoing(time_zone__node_id, 'Schema__MGraph__Time_Series__Edge__UTC_Offset')
                return data.node(utc_offset__node_id)

        point_1__node_id = point_1.node_id
        point_2__node_id = point_2.node_id

        utc_offset_1__node = get_utc_offset_from_point(point_1__node_id)
        utc_offset_2__node = get_utc_offset_from_point(point_2__node_id)

        assert utc_offset_1__node.node_id == utc_offset_2__node.node_id                   # these should be the same :)
        assert utc_offset_1__node.node_data.value == -300                                 # offset should be -300 (i.e 5h = 5 * 60)