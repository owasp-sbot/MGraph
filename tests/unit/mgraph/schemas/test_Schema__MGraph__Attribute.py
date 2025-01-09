from unittest                                           import TestCase
from typing                                             import  Any
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute import Schema__MGraph__Attribute
from osbot_utils.helpers.Random_Guid                    import Random_Guid
from osbot_utils.helpers.Safe_Id                        import Safe_Id

class test_Schema__MGraph__Attribute(TestCase):

    def setUp(self):    # Initialize test data
        self.attribute_id    = Random_Guid()
        self.attribute_name  = Safe_Id('test_attr')
        self.attribute_value = "test_value"
        self.attribute_type  = str
        self.attribute      = Schema__MGraph__Attribute(attribute_id    = self.attribute_id   ,
                                                        attribute_name  = self.attribute_name ,
                                                        attribute_value = self.attribute_value,
                                                        attribute_type  = self.attribute_type )

    def test_init(self):                                                        # Tests basic initialization and type checking
        assert type(self.attribute)            is Schema__MGraph__Attribute
        assert self.attribute.attribute_id     == self.attribute_id
        assert self.attribute.attribute_name   == self.attribute_name
        assert self.attribute.attribute_value  == self.attribute_value
        assert self.attribute.attribute_type   == self.attribute_type

    def test_type_safety_validation(self):                                      # Tests type safety validations
        with self.assertRaises(ValueError) as context:                         # Test invalid Random_Guid
            Schema__MGraph__Attribute(attribute_id   = 'invalid-guid'      ,
                                     attribute_name  = self.attribute_name ,
                                     attribute_value = self.attribute_value,
                                     attribute_type  = self.attribute_type )
        assert 'value provided was not a Guid' in str(context.exception)

        # Test Safe_Id conversion
        attribute = Schema__MGraph__Attribute(attribute_id    = Random_Guid()       ,
                                              attribute_name  = 'unsafe!@#id'       ,
                                              attribute_value = self.attribute_value,
                                              attribute_type  = self.attribute_type )
        assert type(attribute.attribute_name) is Safe_Id
        assert str(attribute.attribute_name)  == 'unsafe___id'

    def test_various_attribute_types(self):    # Tests creation of attributes with different value types
        test_cases = [
            (42,               int,  "integer"),
            (True,             bool, "boolean"),
            (3.14,             float, "float"),
            (["a", "b"],       list, "list"),
            ({"key": "value"}, dict, "dictionary"),
            (None,             Any,  "None with Any type")
        ]

        for value, type_, desc in test_cases:
            with self.subTest(description=desc):
                attribute = Schema__MGraph__Attribute(
                    attribute_id    = Random_Guid(),
                    attribute_name  = Safe_Id(f'test_{desc}'),
                    attribute_value = value,
                    attribute_type  = type_
                )
                assert attribute.attribute_value == value
                assert attribute.attribute_type  == type_

    def test_serialization(self):    # Tests JSON serialization and deserialization
        json_data = self.attribute.json()

        # Verify JSON structure
        assert 'attribute_id'    in json_data
        assert 'attribute_name'  in json_data
        assert 'attribute_value' in json_data
        assert 'attribute_type'  in json_data

        # Test deserialization
        restored = Schema__MGraph__Attribute.from_json(json_data)
        assert restored.attribute_id    == self.attribute.attribute_id
        assert restored.attribute_name  == self.attribute.attribute_name
        assert restored.attribute_value == self.attribute.attribute_value
        assert restored.attribute_type  == self.attribute.attribute_type