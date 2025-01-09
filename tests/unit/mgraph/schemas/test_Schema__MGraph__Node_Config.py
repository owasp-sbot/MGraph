from unittest                                              import TestCase
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node_Config  import Schema__MGraph__Node_Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node         import Schema__MGraph__Node
from osbot_utils.helpers.Random_Guid                       import Random_Guid

class Simple_Node(Schema__MGraph__Node): pass           # Helper class for testing

class test_Schema__MGraph__Node_Config(TestCase):

    def setUp(self):    # Initialize test data
        self.node_id    = Random_Guid()
        self.value_type = str
        self.node_config = Schema__MGraph__Node_Config(node_id    = self.node_id   ,
                                                       value_type = self.value_type)

    def test_init(self):                                                                    # Tests basic initialization and type checking
        assert type(self.node_config)           is Schema__MGraph__Node_Config
        assert self.node_config.node_id         == self.node_id
        assert self.node_config.value_type      == self.value_type

    def test_type_safety_validation(self):                                                  # Tests type safety validations
        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Node_Config(node_id    = "not-a-guid",                          # Should be Random_Guid
                                      value_type = self.value_type)
        assert str(context.exception) == "in Random_Guid: value provided was not a Guid: not-a-guid"

        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Node_Config(node_id    = self.node_id,
                                      value_type = "not-a-type")                            # Should be type
        assert 'Invalid type for attribute' in str(context.exception)

    def test_different_value_types(self):    # Tests different value type combinations
        node_config_1 = Schema__MGraph__Node_Config(node_id    = Random_Guid(),
                                                  value_type = dict        )
        assert node_config_1.value_type == dict

        class CustomValueType: pass

        node_config_2 = Schema__MGraph__Node_Config(node_id    = Random_Guid()  ,
                                                    value_type = CustomValueType)
        assert node_config_2.value_type == CustomValueType

        node_config_3 = Schema__MGraph__Node_Config(node_id    = Random_Guid(),
                                                  value_type = int         )
        assert node_config_3.value_type == int