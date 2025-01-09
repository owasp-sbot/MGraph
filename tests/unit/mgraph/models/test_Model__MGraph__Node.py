from unittest                                             import TestCase
from mgraph_ai.mgraph.models.Model__MGraph__Node          import Model__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node        import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node_Config import Schema__MGraph__Node_Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute   import Schema__MGraph__Attribute
from osbot_utils.helpers.Random_Guid                      import Random_Guid
from osbot_utils.helpers.Safe_Id                          import Safe_Id

class test_Model__MGraph__Node(TestCase):

    def setUp(self):                                                                            # Initialize test data
        self.node_config = Schema__MGraph__Node_Config(node_id    = Random_Guid(),
                                                       value_type = str         )
        self.node = Schema__MGraph__Node              (attributes  = {}                  ,
                                                       node_config = self.node_config    ,
                                                       node_type   = Schema__MGraph__Node,
                                                       value      = "test_value"         )
        self.model = Model__MGraph__Node(data=self.node)

    def test_init(self):                                                                        # Tests basic initialization
        assert type(self.model)   is Model__MGraph__Node
        assert self.model.data    is self.node
        assert self.model.value() == "test_value"

    def test_set_value_with_type_check(self):                                                   # Tests value setting with type validation
        # Test valid value type
        self.model.set_value("new_value")
        assert self.model.value() == "new_value"

        # Test invalid value type
        with self.assertRaises(TypeError) as context:
            self.model.set_value(123)
        assert str(context.exception) == "Value must be of type <class 'str'>"

    def test_set_value_without_type_check(self):                                                # Tests value setting without type validation
        node_config = Schema__MGraph__Node_Config(
            node_id    = Random_Guid(),
            value_type = None
        )
        node = Schema__MGraph__Node(
            attributes  = {},
            node_config = node_config,
            node_type   = Schema__MGraph__Node,
            value      = "test_value"
        )
        model = Model__MGraph__Node(data=node)

        # Should accept any type when value_type is None
        model.set_value(123)
        assert model.value() == 123

        model.set_value("string")
        assert model.value() == "string"

        model.set_value(True)
        assert model.value() == True

    def test_attribute_management(self):                                                        # Tests attribute addition and retrieval
        attribute = Schema__MGraph__Attribute(
            attribute_id    = Random_Guid(),
            attribute_name  = Safe_Id('test_attr'),
            attribute_value = "attr_value",
            attribute_type  = str
        )

        # Test adding attribute
        self.model.add_attribute(attribute)
        assert len(self.model.data.attributes) == 1

        # Test retrieving attribute
        retrieved = self.model.attribute(attribute.attribute_id)
        assert retrieved == attribute

        # Test retrieving non-existent attribute
        non_existent = self.model.attribute(Random_Guid())
        assert non_existent is None