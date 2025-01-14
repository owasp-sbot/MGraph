import unittest
from osbot_utils.utils.Objects                                   import __
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node import (
    Schema__MGraph__Json__Node         ,
    Schema__MGraph__Json__Node__Value  ,
    Schema__MGraph__Json__Node__Dict   ,
    Schema__MGraph__Json__Node__List   ,
    Schema__MGraph__Json__Node__Property,
    Schema__MGraph__Json__Node__Value__Data,
    Schema__MGraph__Json__Node__Property__Data
)

class test_Schema__MGraph__Json__Node(unittest.TestCase):
    def test__init__(self):                                                                         # Test base JSON node initialization
        with Schema__MGraph__Json__Node() as _:
            assert _.obj() == __(node_data  =__(),
                                 node_type  = 'mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node.Schema__MGraph__Json__Node',
                                 node_id    = _.node_id)

class test_Schema__MGraph__Json__Node__Value(unittest.TestCase):
    def test__init__(self):                                                                         # Test Value node initialization
        with Schema__MGraph__Json__Node__Value() as _:
            assert _.obj() == __(node_data  =__(value      = None   ,
                                                value_type = None   ),
                                 node_type  = 'mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node.Schema__MGraph__Json__Node__Value',
                                 node_id    = _.node_id)

    def test_value_node_creation(self):                                                             # Test creating a value node with different types of values
        test_cases = [ ("hello"   , str       ),
                       (42        , int       ),
                       (3.14      , float     ),
                       (True      , bool      ),
                       (None      , type(None))]

        for value, expected_type in test_cases:
            node_data = Schema__MGraph__Json__Node__Value__Data(value=value,
                                                                value_type=expected_type)
            node = Schema__MGraph__Json__Node__Value(node_data=node_data)

            assert node.node_data.value      == value
            assert node.node_data.value_type == expected_type
            assert node.node_type            == Schema__MGraph__Json__Node__Value

class test_Schema__MGraph__Json__Node__Dict(unittest.TestCase):
    def test__init__(self):                                                                         # Test Dict node initialization
        with Schema__MGraph__Json__Node__Dict() as _:
            assert _.obj() == __(node_data  =__(),
                                 node_type  = 'mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node.Schema__MGraph__Json__Node__Dict',
                                 node_id    = _.node_id)

class test_Schema__MGraph__Json__Node__List(unittest.TestCase):
    def test__init__(self):                                                                         # Test List node initialization
        with Schema__MGraph__Json__Node__List() as _:
            assert _.obj() == __(node_data  =__(),
                                 node_type  = 'mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node.Schema__MGraph__Json__Node__List',
                                 node_id    = _.node_id)

class test_Schema__MGraph__Json__Node__Property(unittest.TestCase):
    def test__init__(self):                                                                         # Test Property node initialization
        with Schema__MGraph__Json__Node__Property() as _:
            assert _.obj() == __(node_data  =__(name=''),
                                 node_type  = 'mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node.Schema__MGraph__Json__Node__Property',
                                 node_id    = _.node_id)

    def test_property_node_creation(self):                                                          # Test creating a property node
        node_data = Schema__MGraph__Json__Node__Property__Data(name='test_property')
        node = Schema__MGraph__Json__Node__Property(node_data=node_data)

        assert node.node_data.name  == "test_property"
        assert node.node_type       == Schema__MGraph__Json__Node__Property

    def test_property_node_name_change(self):                                                       # Test changing a property node's name
        node_data = Schema__MGraph__Json__Node__Property__Data(name='original_name')
        node = Schema__MGraph__Json__Node__Property(node_data=node_data)

        node.node_data.name = "new_name"
        assert node.node_data.name == "new_name"

class Test_Schema__MGraph__Json__Node_Inheritance(unittest.TestCase):
    def test_base_node_inheritance(self):                                                           # Verify that all specific node types inherit from base JSON node
        node_classes = [
            Schema__MGraph__Json__Node__Value,
            Schema__MGraph__Json__Node__Dict,
            Schema__MGraph__Json__Node__List,
            Schema__MGraph__Json__Node__Property
        ]

        for node_class in node_classes:
            assert issubclass(node_class, Schema__MGraph__Json__Node), \
                f"{node_class.__name__} should inherit from Schema__MGraph__Json__Node"