import pytest
import unittest
from osbot_utils.utils.Objects                                   import __, type_full_name
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node import (
    Schema__MGraph__Json__Node__Value__Data,
    Schema__MGraph__Json__Node__Value,
    Schema__MGraph__Json__Node__Property__Data,
    Schema__MGraph__Json__Node__Property,
    Schema__MGraph__Json__Node__Dict,
    Schema__MGraph__Json__Node__List, Schema__MGraph__Json__Node
)
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node import (
    Model__MGraph__Json__Node__Value,
    Model__MGraph__Json__Node__Property,
    Model__MGraph__Json__Node__Dict,
    Model__MGraph__Json__Node__List,
    Model__MGraph__Json__Node
)

class test_Model__MGraph__Json__Node(unittest.TestCase):
    def test_init(self):                                                                                # Test base JSON node model initialization
        with Model__MGraph__Json__Node(data=Schema__MGraph__Json__Node()) as _:                         # Create base JSON node model
            assert _.obj()                == __(data=__(node_data  = __()     ,
                                                        node_id    = _.node_id,
                                                        node_type  = type_full_name(Schema__MGraph__Json__Node)))
            assert _.data.node_type       == Schema__MGraph__Json__Node
            assert _.obj().data.node_type == type_full_name(Schema__MGraph__Json__Node)
            assert _.obj().data.node_type == 'mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node.Schema__MGraph__Json__Node'

class test_Model__MGraph__Json__Node__Value(unittest.TestCase):
    def test_init(self):                                                                            # Test base JSON value node model initialization
        with Model__MGraph__Json__Node__Value(data=Schema__MGraph__Json__Node__Value()) as _:        # Create base JSON value node model
            assert _.obj() == __(data = __(node_data = __(value      = None ,
                                                          value_type = None),
                                           node_id   = _.data.node_id,
                                           node_type = type_full_name(Schema__MGraph__Json__Node__Value)))

    def test_value_node_creation(self):                                                             # Test creating a value node model
        node_data   = Schema__MGraph__Json__Node__Value__Data(value="hello", value_type=str)        # Create schema node with value data
        schema_node = Schema__MGraph__Json__Node__Value(node_data=node_data)                        # Create schema node

        # Create model node
        model_node = Model__MGraph__Json__Node__Value(data=schema_node)                             # Create model node

        # Verify properties
        assert model_node.value == "hello"
        assert model_node.value_type == str
        assert model_node.is_primitive() is True

    def test_value_and_type_updates(self):                                                          # Create schema node with initial value
        node_data   = Schema__MGraph__Json__Node__Value__Data(value=42, value_type=int)
        schema_node = Schema__MGraph__Json__Node__Value(node_data=node_data)
        model_node  = Model__MGraph__Json__Node__Value(data=schema_node)

        assert model_node.value == 42                                                               # Verify initial state
        assert model_node.value_type == int


        model_node.value = "new value"                                                              # Update with different types and verify type is automatically updated
        assert model_node.value      == "new value"
        assert model_node.value_type == str

        model_node.value = 3.14
        assert model_node.value      == 3.14
        assert model_node.value_type == float

        model_node.value = True
        assert model_node.value      == True
        assert model_node.value_type == bool

        with pytest.raises(ValueError, match="Can't set None, to a variable that is already set. Invalid type for attribute 'value'. Expected 'typing.Any' but got '<class 'NoneType'>'"):
            model_node.value        = None

    def test_primitive_check(self):                                                                 # Test primitive type detection
        # Test various primitive types
        test_cases = [(42       , int, True        ),
                      (3.14     , float, True      ),
                      ("hello"  , str, True        ),
                      (True     , bool, True       ),
                      (None     , type(None), True )]

        for value, value_type, expected_primitive in test_cases:                                    # Iterate through test cases
            node_data = Schema__MGraph__Json__Node__Value__Data(value=value, value_type=value_type) # Create node data
            schema_node = Schema__MGraph__Json__Node__Value(node_data=node_data)                    # Create schema node
            model_node = Model__MGraph__Json__Node__Value(data=schema_node)                         # Create model node

            assert model_node.is_primitive() is expected_primitive

class test_Model__MGraph__Json__Node__Dict(unittest.TestCase):

    def test_init(self):                                                                            # Test base JSON dict node model initialization
        with Model__MGraph__Json__Node__Dict(data=Schema__MGraph__Json__Node__Dict()) as _:          # Create base JSON dict node model
            assert _.obj() == __(data = __(node_data = __()     ,
                                           node_id    = _.node_id,
                                           node_type  = type_full_name(Schema__MGraph__Json__Node__Dict)))

class test_Model__MGraph__Json__Node__List(unittest.TestCase):

    def test_init(self):                                                                            # Test base JSON list node model initialization
        with Model__MGraph__Json__Node__List(data=Schema__MGraph__Json__Node__List()) as _:          # Create base JSON list node model
            assert _.obj() == __(data = __(node_data = __()     ,
                                           node_id    = _.node_id,
                                           node_type  = type_full_name(Schema__MGraph__Json__Node__List)))

class test_Model__MGraph__Json__Node__Property(unittest.TestCase):
    @classmethod

    def test_init(self):                                                                            # Test base JSON property node model initialization
        with Model__MGraph__Json__Node__Property(data=Schema__MGraph__Json__Node__Property()) as _:  # Create base JSON property node model
            assert _.obj() == __(data =__(node_data = __(name = ''),
                                         node_id    = _.node_id,
                                         node_type  = type_full_name(Schema__MGraph__Json__Node__Property)))

    def test_property_node_creation(self):                                                          # Test creating a property node model
        # Create schema node with property data
        node_data = Schema__MGraph__Json__Node__Property__Data(name='test_property')                # Create schema node with property data
        schema_node = Schema__MGraph__Json__Node__Property(node_data=node_data)                     # Create schema node

        # Create model node
        model_node = Model__MGraph__Json__Node__Property(data=schema_node)                          # Create model node

        # Verify properties
        assert model_node.name == "test_property"

    def test_set_property_name(self):                                                               # Test changing property name
        # Create schema node with initial name
        node_data = Schema__MGraph__Json__Node__Property__Data(name='original_name')                # Create schema node with initial name
        schema_node = Schema__MGraph__Json__Node__Property(node_data=node_data)                     # Create schema node

        # Create model node
        model_node = Model__MGraph__Json__Node__Property(data=schema_node)                          # Create model node

        # Change name
        model_node.name = "new_name"                                                                # Change property name

        # Verify updated properties
        assert model_node.name == "new_name"
        assert model_node.data.node_data.name == "new_name"