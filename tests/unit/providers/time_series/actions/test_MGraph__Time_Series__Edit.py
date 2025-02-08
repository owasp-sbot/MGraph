import pytest
from unittest                                                                       import TestCase
from mgraph_db.mgraph.actions.MGraph__Export                                        import MGraph__Export
from mgraph_db.mgraph.actions.MGraph__Index import MGraph__Index
from mgraph_db.mgraph.actions.exporters.MGraph__Export__Dot                         import MGraph__Export__Dot
from mgraph_db.mgraph.domain.Domain__MGraph__Node                                   import Domain__MGraph__Node
from mgraph_db.mgraph.models.Model__MGraph__Graph                                   import Model__MGraph__Graph
from mgraph_db.mgraph.models.Model__MGraph__Node                                    import Model__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph                                 import Schema__MGraph__Graph
from mgraph_db.providers.time_series.MGraph__Time_Series                            import MGraph__Time_Series
from mgraph_db.providers.time_series.actions.MGraph__Time_Series__Edit              import MGraph__Time_Series__Edit
from mgraph_db.providers.time_series.actions.MGraph__Time_Series__Screenshot        import MGraph__Time_Series__Screenshot
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Time_Point       import Schema__MGraph__Node__Time_Point
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Value__Int       import Schema__MGraph__Node__Value__Int
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Value__Int__Data import Schema__MGraph__Node__Value__Int__Data
from mgraph_db.providers.time_series.schemas.Schema__MGraph__TimeSeries__Edges      import (Schema__MGraph__Time_Series__Edge__Year,
                                                                                           Schema__MGraph__Time_Series__Edge__Month,
                                                                                           Schema__MGraph__Time_Series__Edge__Day,
                                                                                           Schema__MGraph__Time_Series__Edge__Hour,
                                                                                           Schema__MGraph__Time_Series__Edge__Minute)
from osbot_utils.utils.Dev                                                          import pprint
from osbot_utils.utils.Env                                                          import load_dotenv
from osbot_utils.utils.Files                                                        import file_exists, file_delete
from osbot_utils.utils.Objects                                                      import __, type_full_name
from osbot_utils.helpers.Obj_Id                                                     import is_obj_id, Obj_Id


class test_MGraph__Time_Series__Edit(TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.screenshot_create = False
        cls.screenshot_file  = './time-series.png'
        cls.screenshot_delete = False

    def setUp(self):
        self.graph       = MGraph__Time_Series()                                                    # Create fresh graph
        self.graph_edit = self.graph.edit()                                                        # Get edit interface

    def tearDown(self):
        if self.screenshot_create:
            with self.graph.screenshot(target_file=self.screenshot_file) as _:
                assert type(_)                       is MGraph__Time_Series__Screenshot
                assert type(_.export().export_dot()) is MGraph__Export__Dot
                assert _.export_class               is MGraph__Export

                (_.export().export_dot()
                          .show_node__value        ()
                          .set_node__style__filled ()
                          .set_node__color         ('#0000ff80')
                          .set_node__font__size(10)
                          .set_node__type_color    ('Schema__MGraph__Node__Time_Point', 'azure')
                          .set_node__type_shape    ('Schema__MGraph__Node__Time_Point', 'box'    )
                          .set_node__type_style    ('Schema__MGraph__Node__Time_Point', 'filled,rounded' ))

                _.dot()
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
                                    Schema__MGraph__Time_Series__Edge__Minute: 'minute'}

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