from unittest                                           import TestCase
from osbot_utils.helpers.Safe_Id                        import Safe_Id
from mgraph_ai.mgraph.domain.Domain__MGraph__Attribute          import Domain__MGraph__Attribute
from mgraph_ai.mgraph.models.Model__MGraph__Attribute   import Model__MGraph__Attribute
from mgraph_ai.mgraph.models.Model__MGraph__Graph       import Model__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute import Schema__MGraph__Attribute
from osbot_utils.helpers.Random_Guid                    import Random_Guid

class test_MGraph__Attribute(TestCase):

    def setUp(self):                                                                        # Initialize test data
        self.graph = Model__MGraph__Graph(data=None)                                        # Mock graph for testing

        # Create schema attribute
        self.schema_attribute = Schema__MGraph__Attribute(attribute_id    = Random_Guid()       ,
                                                          attribute_name  = Safe_Id('test_attr'),
                                                          attribute_value = "test_value"        ,
                                                          attribute_type  = str                 )

        # Create model and domain attribute
        self.model_attribute = Model__MGraph__Attribute(data=self.schema_attribute)
        self.attribute       = Domain__MGraph__Attribute(attribute=self.model_attribute, graph=self.graph)

    def test_init(self):                                                                    # Tests basic initialization
        assert type(self.attribute) is Domain__MGraph__Attribute
        assert self.attribute.attribute  is self.model_attribute
        assert self.attribute.graph      is self.graph
        assert type(self.attribute.id()) is Random_Guid
        assert self.attribute.name()     == str(self.schema_attribute.attribute_name)
        assert self.attribute.value()    == "test_value"

    def test_value_operations(self):                                                        # Tests value getting and setting
        assert self.attribute.value() == "test_value"

        self.attribute.set_value("new_value")
        assert self.attribute.value() == "new_value"

        with self.assertRaises(TypeError) as context:                                      # Test type validation
            self.attribute.set_value(42)
        assert "Value must be of type" in str(context.exception)

    def test_setting_values_with_different_types(self):                                     # Tests value setting with different types
        test_cases = [("string_value", str  ),
                      (42,             int  ),
                      (True,           bool ),
                      (3.14,           float)]

        for value, expected_type in test_cases:
            # Create a new attribute with specific type
            schema_attr = Schema__MGraph__Attribute(attribute_id    = Random_Guid()       ,
                                                    attribute_name  = Safe_Id('test_attr'),
                                                    attribute_value = value               ,
                                                    attribute_type  = expected_type       )
            model_attr = Model__MGraph__Attribute(data=schema_attr)
            attr = Domain__MGraph__Attribute(attribute=model_attr, graph=self.graph)

            assert attr.value() == value
            assert attr.attribute.data.attribute_type == expected_type

            # Verify type validation works
            attr.set_value(value)  # Should work with matching type

            with self.assertRaises(TypeError):
                attr.set_value(b"wrong_type")  # Should raise error for incorrect type

    def test_type_less_attribute(self):                                                     # Tests attribute without type constraint
        schema_attr = Schema__MGraph__Attribute(attribute_id    = Random_Guid()       ,     # Create attribute with no type constraint
                                                attribute_name  = Safe_Id('test_attr'),
                                                attribute_value = "initial_value"     ,
                                                attribute_type  = None                )
        model_attr = Model__MGraph__Attribute(data=schema_attr)
        attr      = Domain__MGraph__Attribute(attribute=model_attr, graph=self.graph)

        # Should allow setting different types of values
        test_values = ["string", 42, True, 3.14]
        for value in test_values:
            attr.set_value(value)
            assert attr.value() == value