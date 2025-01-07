from unittest                                      import TestCase
from osbot_utils.helpers.Random_Guid               import Random_Guid
from mgraph_ai.schemas.Schema__MGraph__Edge_Config import Schema__MGraph__Edge_Config
from osbot_utils.utils.Misc                        import is_guid
from osbot_utils.utils.Objects                     import __
from mgraph_ai.models.Model__MGraph__Edge          import Model__MGraph__Edge
from mgraph_ai.schemas.Schema__MGraph__Edge        import Schema__MGraph__Edge

class test_Model__MGraph__Edge(TestCase):

    def setUp(self):
        self.edge = Model__MGraph__Edge()                                 # Create a fresh edge model for each test

        # Create sample edge configuration
        self.edge_config = Schema__MGraph__Edge_Config(edge_id        = Random_Guid(),
                                                       from_node_type = str          ,
                                                       to_node_type   = int          )

        # Create sample node IDs
        self.from_node_id = Random_Guid()
        self.to_node_id = Random_Guid()

        # Create sample edge data
        self.edge_data = Schema__MGraph__Edge(
            attributes={},
            edge_config=self.edge_config,
            from_node_id=self.from_node_id,
            to_node_id=self.to_node_id
        )

    def test__init__(self):
        # Test default initialization
        assert type(self.edge) is Model__MGraph__Edge
        assert type(self.edge.data) is Schema__MGraph__Edge
        assert isinstance(self.edge.data.edge_config.edge_id, Random_Guid)

        # Test initialization with provided data
        edge_model = Model__MGraph__Edge(data=self.edge_data)
        assert edge_model.data == self.edge_data
        assert edge_model.data.edge_config == self.edge_config
        assert edge_model.data.from_node_id == self.from_node_id
        assert edge_model.data.to_node_id == self.to_node_id

        with self.edge.data as _:
            edge_id = _.edge_config.edge_id
            assert type(_) is Schema__MGraph__Edge
            assert _.obj() == __(attributes     = __()                   ,
                                 edge_config=__(edge_id        = edge_id,
                                                from_node_type = None   ,
                                                to_node_type   = None   ),
                                 from_node_id   = _.from_node_id         ,
                                 to_node_id     = _.to_node_id           )
            assert is_guid(edge_id       )
            assert is_guid(_.from_node_id)
            assert is_guid(_.to_node_id  )

    def test_attributes_manipulation(self):
        # Create a test attribute
        attr_id = Random_Guid()
        attr = Schema__MGraph__Attribute(
            attribute_id=attr_id,
            attribute_name=Safe_Id('test_attr'),
            attribute_value="test_value",
            attribute_type=str
        )

        # Add attribute to edge
        self.edge.data.attributes[attr_id] = attr

        # Verify attribute was added correctly
        assert len(self.edge.data.attributes) == 1
        assert self.edge.data.attributes[attr_id] == attr
        assert self.edge.data.attributes[attr_id].attribute_value == "test_value"

    def test_type_safety(self):
        # Test that type safety is enforced for edge data
        with self.assertRaises(ValueError):
            Model__MGraph__Edge(data="not_an_edge")  # Should fail as data must be Schema__MGraph__Edge

        # Test type safety for attributes
        invalid_attr = "not_an_attribute"
        with self.assertRaises(ValueError):
            self.edge.data.attributes[Random_Guid()] = invalid_attr

    def test_edge_configuration(self):
        # Test edge configuration modification
        new_edge_config = Schema__MGraph__Edge_Config(
            edge_id=Random_Guid(),
            from_node_type=bool,
            to_node_type=list
        )
        self.edge.data.edge_config = new_edge_config

        assert self.edge.data.edge_config == new_edge_config
        assert self.edge.data.edge_config.from_node_type == bool
        assert self.edge.data.edge_config.to_node_type == list

    def test_node_connections(self):
        # Test modifying node connections
        new_from_node = Random_Guid()
        new_to_node = Random_Guid()

        self.edge.data.from_node_id = new_from_node
        self.edge.data.to_node_id = new_to_node

        assert self.edge.data.from_node_id == new_from_node
        assert self.edge.data.to_node_id == new_to_node

    def test_serialization(self):
        # Test serialization to dictionary
        edge_dict = self.edge.json()

        assert isinstance(edge_dict, dict)
        assert 'data' in edge_dict
        assert 'edge_config' in edge_dict['data']
        assert 'attributes' in edge_dict['data']
        assert 'from_node_id' in edge_dict['data']
        assert 'to_node_id' in edge_dict['data']

        # Test deserialization
        new_edge_model = Model__MGraph__Edge.from_json(edge_dict)
        assert isinstance(new_edge_model, Model__MGraph__Edge)
        assert new_edge_model.data.edge_config.edge_id == self.edge.data.edge_config.edge_id


