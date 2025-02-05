import pytest
from unittest                                                                       import TestCase
from mgraph_db.mgraph.actions.MGraph__Export                                        import MGraph__Export
from mgraph_db.mgraph.actions.exporters.MGraph__Export__Dot                         import MGraph__Export__Dot
from mgraph_db.mgraph.domain.Domain__MGraph__Node                                   import Domain__MGraph__Node
from mgraph_db.mgraph.models.Model__MGraph__Graph                                   import Model__MGraph__Graph
from mgraph_db.mgraph.models.Model__MGraph__Node                                    import Model__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph                                 import Schema__MGraph__Graph
from mgraph_db.providers.time_series.MGraph__Time_Series                            import MGraph__Time_Series
from mgraph_db.providers.time_series.actions.MGraph__Time_Series__Edit              import MGraph__Time_Series__Edit
from mgraph_db.providers.time_series.actions.MGraph__Time_Series__Screenshot        import MGraph__Time_Series__Screenshot
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Value__Int       import Schema__MGraph__Node__Value__Int
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Value__Int__Data import Schema__MGraph__Node__Value__Int__Data
from osbot_utils.utils.Dev                                                          import pprint
from osbot_utils.utils.Env                                                          import load_dotenv
from osbot_utils.utils.Files                                                        import file_exists, file_delete
from osbot_utils.utils.Objects                                                      import __, type_full_name
from osbot_utils.helpers.Obj_Id                                                     import is_obj_id, Obj_Id


class test_MGraph__Time_Series__Edit(TestCase):

    @classmethod
    def setUpClass(cls):
        pytest.skip("Tests need fixing after Time_Series class is fixed")
        load_dotenv()
        cls.screenshot_create = True
        cls.screenshot_file   = './time-series.png'
        cls.screenshot_delete = False

    def setUp(self):
        self.graph       = MGraph__Time_Series()                                                          # Create fresh graph
        self.graph_edit = self.graph.edit()                                                              # Get edit interface


    def tearDown(self):
        # with self.graph.data() as _:
        #     _.print()
        if self.screenshot_create:
            with self.graph.screenshot(target_file=self.screenshot_file) as _:
                assert type(_)                       is MGraph__Time_Series__Screenshot
                assert type(_.export().export_dot()) is MGraph__Export__Dot
                assert _.export_class               is MGraph__Export

                (_.export().export_dot()#.show_node__type        ()
                                        .show_node__value        ()
                                        #.hide_edge__ids          ()
                                        #.set_node__shape__box    ()
                                        #.set_node__shape__underline()
                                        .set_node__style__filled ()
                                        #.set_node__style__rounded()
                                        .set_node__color         ('#0000ff80').set_node__font__size(10)
                                        #.set_font__color         ('white'   ).set_node__font__bold()
                                        .set_node__type_color    ('Schema__MGraph__Node__Time_Point', 'azure')
                                        .set_node__type_shape    ('Schema__MGraph__Node__Time_Point', 'box'    )
                                        .set_node__type_style    ('Schema__MGraph__Node__Time_Point', 'filled,rounded' )
                )


                #_.dot__just_types()
                #_.dot__just_values()

                print()
                print(_.export().to__dot())
                _.dot()
                assert file_exists(self.screenshot_file) is True
                if self.screenshot_delete:
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


    def test__setUp(self):
        with self.graph_edit as _:
            assert type(_) is MGraph__Time_Series__Edit

    def test_find_int_value(self):
        with self.graph_edit as _:
            assert _.find_int_value(42) is None                                                                         # Test when no values exist, should return None for non-existent value

            test_value = 42                                                                                             # Create a value node
            value_node = _.new_node(node_type = Schema__MGraph__Node__Value__Int,                                       # Create value node
                                    value     = test_value                      )                                       # with test_value set
            value_node_id = value_node.node_id
            assert type(value_node          ) is Domain__MGraph__Node
            assert type(value_node.node     ) is Model__MGraph__Node
            assert type(value_node.node.data) is Schema__MGraph__Node__Value__Int                                       # confirm the node is *_Value__Int
            assert type(value_node.node_data) is Schema__MGraph__Node__Value__Int__Data                                 # confirm the node's data is *_Value__Int__Data
            assert value_node.node.obj()      == __(data      =  __(node_data=__(value=42)  ,                           # confirm value has been correctly set
                                                    node_id   = value_node_id               ,
                                                    node_type = type_full_name(Schema__MGraph__Node__Value__Int)))      # and it is of the correct type

            assert _.index().index_data.nodes_by_field == {}                                                            # at this stage the index will be empty (note that .index() is uses @cache_on_self to prevent the index from being created everytime we call this method)
            _.index().add_node(value_node.node.data)                                                                    # the new node needs to be added to the index
            assert _.index().index_data.nodes_by_field == {'value': {42: { value_node_id }}}                            # confirm that the new node is now on the index

            found_id = _.find_int_value(test_value)                                                                     # now we can check if finding existing value
            assert found_id == value_node.node_id                                                                       # returns the correct value (which it does)

            other_values = [10, 20, 30]                                                                                 # Create multiple values and test finding specific one
            for value in other_values:
                new_node = _.new_node(node_type = Schema__MGraph__Node__Value__Int,
                                      value     = value)                                                                # Create additional nodes
                _.index().add_node(new_node.node.data)                                                                  # and add them to the index

            found_id = _.find_int_value(test_value)                                                                     # Should still find original value
            assert found_id == value_node.node_id

            found_id = _.find_int_value(20)                                                                             # Test finding one of the other values
            assert type(found_id) is Obj_Id
            assert _.find_int_value(20) is not None                                                                     # Should find the value
            assert _.find_int_value(21) is     None                                                                     # and not find this one
            node_with_20 = _.data().node(found_id)                                                                      # get the node from the current graph
            assert type(node_with_20          ) is Domain__MGraph__Node                                                 # check its types and values
            assert type(node_with_20.node     ) is Model__MGraph__Node
            assert type(node_with_20.node.data) is Schema__MGraph__Node__Value__Int
            assert type(node_with_20.node_data) is Schema__MGraph__Node__Value__Int__Data                               # Should be correct type
            assert node_with_20.node_data.value == 20                                                                   # Should have correct value

            assert _.find_int_value(999) is None                                                                        # Test non-existent value again
            assert _.data().node(_.find_int_value(10)).node_data.value == 10                                            # check all 3 values previous created
            assert _.data().node(_.find_int_value(20)).node_data.value == 20
            assert _.data().node(_.find_int_value(30)).node_data.value == 30

    def test__get_or_create_int_value(self):
        with self.graph_edit as _:
            value = 42
            assert _.find_int_value(value) is None                                              # confirm that we can't find {value} (before {value} is added)
            node_id = _.get_or_create_int_value(value)                                          # this will create the node (because it doesn't exist)
            node    = _.data().node(node_id)                                                    # get the node from the data object
            assert node.node_id                       == node_id                                # confirm is the one we added before
            assert type(node_id                     ) is Obj_Id                                 # and that it contain the expected objects
            assert type(node                        ) is Domain__MGraph__Node
            assert type(node.graph                  ) is Model__MGraph__Graph
            assert type(node.graph.data             ) is Schema__MGraph__Graph
            assert type(node.node                   ) is Model__MGraph__Node
            assert type(node.node.data              ) is Schema__MGraph__Node__Value__Int
            assert type(node.node.data.node_data    ) is Schema__MGraph__Node__Value__Int__Data

            assert len(_.data().nodes_ids())          == 1                                      # confirm that we only have one node
            assert _.find_int_value(value)            == node_id                                # confirm that calling find_int_value returns the same node_id
            assert _.get_or_create_int_value(value)   == node_id                                # and that get_or_create_int_value is still working as before
            assert len(_.data().nodes_ids())          == 1                                      # confirm the node's size hasn't changed












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