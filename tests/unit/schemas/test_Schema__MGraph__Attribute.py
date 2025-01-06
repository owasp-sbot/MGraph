from unittest                                    import TestCase
from mgraph_ai.schemas.Schema__MGraph__Attribute import Schema__MGraph__Attribute
from osbot_utils.helpers.Random_Guid             import Random_Guid
from osbot_utils.helpers.Safe_Id                 import Safe_Id

class test_Schema__MGraph__Attribute(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.attribute_id    = Random_Guid()
        cls.attribute_name  = Safe_Id('test_attr')
        cls.attribute_value = "test_value"
        cls.attribute_type  = str

    def setUp(self):
        self.attribute = Schema__MGraph__Attribute(
            attribute_id    = self.attribute_id   ,
            attribute_name  = self.attribute_name ,
            attribute_value = self.attribute_value,
            attribute_type  = self.attribute_type )

    def test__init__(self):
        assert type(self.attribute) is Schema__MGraph__Attribute
        assert self.attribute.attribute_id    == self.attribute_id
        assert self.attribute.attribute_name  == self.attribute_name
        assert self.attribute.attribute_value == self.attribute_value
        assert self.attribute.attribute_type  == self.attribute_type

    def test_type_safety(self):
        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Attribute(attribute_id    = 'not-a-guid'       ,          # Should be Random_Guid
                                      attribute_name  = self.attribute_name ,
                                      attribute_value = self.attribute_value,
                                      attribute_type  = self.attribute_type )

        assert str(context.exception) == 'in Random_Guid: value provided was not a Guid: not-a-guid'

        attribute = Schema__MGraph__Attribute(attribute_id    = self.attribute_id   ,
                                              attribute_name  = 'not-a-safe-id(*&(' ,
                                              attribute_value = self.attribute_value,
                                              attribute_type  = self.attribute_type )

        assert type(attribute.attribute_name) is Safe_Id
        assert attribute.attribute_name       == 'not-a-safe-id____'

    def test_different_value_types(self):
        # Test integer attribute
        int_attribute = Schema__MGraph__Attribute(attribute_id    = Random_Guid()       ,
                                                  attribute_name  = Safe_Id('int_attr') ,
                                                  attribute_value = 42                  ,
                                                  attribute_type  = int                 )
        assert int_attribute.attribute_value == 42
        assert int_attribute.attribute_type  == int

        # Test boolean attribute
        bool_attribute = Schema__MGraph__Attribute(attribute_id    = Random_Guid(       ),
                                                   attribute_name  = Safe_Id('bool_attr'),
                                                   attribute_value = True                ,
                                                   attribute_type  = bool                )
        assert bool_attribute.attribute_value is True
        assert bool_attribute.attribute_type  == bool