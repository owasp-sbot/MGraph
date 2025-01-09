from unittest                                           import TestCase
from mgraph_ai.mgraph.models.Model__MGraph__Attribute   import Model__MGraph__Attribute
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute import Schema__MGraph__Attribute
from osbot_utils.helpers.Random_Guid                    import Random_Guid
from osbot_utils.helpers.Safe_Id                        import Safe_Id

class test_Model__MGraph__Attribute(TestCase):

    def setUp(self):                                                                        # Initialize test data
        self.attribute = Schema__MGraph__Attribute(attribute_id    = Random_Guid()       ,
                                                   attribute_name  = Safe_Id('test_attr'),
                                                   attribute_value = "test_value"        ,
                                                   attribute_type  = str                 )
        self.model = Model__MGraph__Attribute(data=self.attribute)

    def test_init(self):                                                                    # Tests basic initialization
        assert type(self.model)      is Model__MGraph__Attribute
        assert self.model.data       is self.attribute
        assert self.model.value()    == "test_value"

    def test_set_value_with_type_check(self):                                               # Tests value setting with type validation
        self.model.set_value("new_value")                                                   # Test valid value type
        assert self.model.value() == "new_value"

        with self.assertRaises(TypeError) as context:                                       # Test invalid value type
            self.model.set_value(123)
        assert str(context.exception) == "Value must be of type <class 'str'>"

    def test_set_value_without_type_check(self):                                            # Tests value setting without type validation
        attribute = Schema__MGraph__Attribute(attribute_id    = Random_Guid()       ,
                                              attribute_name  = Safe_Id('test_attr'),
                                              attribute_value = "test_value"        ,
                                              attribute_type  = None                )
        model = Model__MGraph__Attribute(data=attribute)

        model.set_value(123)                                                                # Should accept any type when attribute_type is None
        assert model.value() == 123

        model.set_value("string")
        assert model.value() == "string"

        model.set_value(True)
        assert model.value() == True