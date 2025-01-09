from unittest                                              import TestCase
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node         import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node_Config  import Schema__MGraph__Node_Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute    import Schema__MGraph__Attribute
from osbot_utils.helpers.Random_Guid                       import Random_Guid
from osbot_utils.helpers.Safe_Id                           import Safe_Id

class test_Schema__MGraph__Node(TestCase):

    def setUp(self):    # Initialize test data
        self.node_config = Schema__MGraph__Node_Config(node_id    = Random_Guid(),
                                                       value_type = str           )

        self.attribute  = Schema__MGraph__Attribute(attribute_id    = Random_Guid()       ,
                                                    attribute_name  = Safe_Id('test_attr'),
                                                    attribute_value = "test_value"        ,
                                                    attribute_type  = str                 )

        self.node      = Schema__MGraph__Node(attributes  = {self.attribute.attribute_id: self.attribute},
                                              node_config = self.node_config                             ,
                                              node_type   = Schema__MGraph__Node                         ,
                                              value      = "test_node_value"                             )

    def test_init(self):                                                                            # Tests basic initialization and type checking
        assert type(self.node)                                  is Schema__MGraph__Node
        assert self.node.node_config                           == self.node_config
        assert self.node.value                                 == "test_node_value"
        assert len(self.node.attributes)                       == 1
        assert self.node.attributes[self.attribute.attribute_id] == self.attribute

    def test_type_safety_validation(self):                                                          # Tests type safety validations
        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Node(attributes  = "not-a-dict"         ,                               # Should be Dict
                                 node_config = self.node_config     ,
                                 node_type   = Schema__MGraph__Node ,
                                 value      = "test_node_value"     )
        assert 'Invalid type for attribute' in str(context.exception)

        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Node(attributes  = {self.attribute.attribute_id: self.attribute},
                                 node_config = "not-a-node-config"                         ,        # Should be Schema__MGraph__Node_Config
                                 node_type   = Schema__MGraph__Node                        ,
                                 value      = "test_node_value"                            )
        assert 'Invalid type for attribute' in str(context.exception)

    def test_different_value_types(self):    # Tests nodes with different value types
        node_config_int = Schema__MGraph__Node_Config(node_id    = Random_Guid(),
                                                      value_type = int          )

        node_int = Schema__MGraph__Node(attributes  = {}                    ,
                                        node_config = node_config_int       ,
                                        node_type   = Schema__MGraph__Node  ,
                                        value      = 42                     )
        assert node_int.value == 42

        node_config_bool = Schema__MGraph__Node_Config(node_id    = Random_Guid(),
                                                     value_type = bool          )

        node_bool = Schema__MGraph__Node(attributes  = {}                    ,
                                       node_config = node_config_bool        ,
                                       node_type   = Schema__MGraph__Node    ,
                                       value      = True                     )
        assert node_bool.value is True

    def test_multiple_attributes(self):    # Tests node with multiple attributes
        attr_1 = Schema__MGraph__Attribute(attribute_id    = Random_Guid()        ,
                                         attribute_name  = Safe_Id('attr_1')    ,
                                         attribute_value = "value_1"            ,
                                         attribute_type  = str                  )

        attr_2 = Schema__MGraph__Attribute(attribute_id    = Random_Guid()        ,
                                         attribute_name  = Safe_Id('attr_2')    ,
                                         attribute_value = 42                   ,
                                         attribute_type  = int                  )

        node = Schema__MGraph__Node(attributes = {attr_1.attribute_id: attr_1,
                                               attr_2.attribute_id: attr_2 },
                                  node_config = self.node_config          ,
                                  node_type   = Schema__MGraph__Node      ,
                                  value      = "test_node_value"          )

        assert len(node.attributes)                == 2
        assert node.attributes[attr_1.attribute_id] == attr_1
        assert node.attributes[attr_2.attribute_id] == attr_2