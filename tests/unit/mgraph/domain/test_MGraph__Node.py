from unittest                                              import TestCase
from osbot_utils.helpers.Safe_Id                           import Safe_Id
from mgraph_ai.mgraph.domain.MGraph__Node                  import MGraph__Node
from mgraph_ai.mgraph.models.Model__MGraph__Node           import Model__MGraph__Node
from mgraph_ai.mgraph.models.Model__MGraph__Graph          import Model__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node         import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Config import Schema__MGraph__Node__Config
from osbot_utils.helpers.Random_Guid                       import Random_Guid

class test_MGraph__Node(TestCase):

    def setUp(self):                                                                        # Initialize test data
        self.node_config = Schema__MGraph__Node__Config(node_id    = Random_Guid(),
                                                        value_type = str)
        self.schema_node = Schema__MGraph__Node       (attributes  = {}                  ,
                                                       node_config = self.node_config    ,
                                                       node_type   = Schema__MGraph__Node,
                                                       value      = "test_value"         )
        self.model_node = Model__MGraph__Node(data=self.schema_node)
        self.graph      = Model__MGraph__Graph(data=None)                                   # Mock graph for testing
        self.node       = MGraph__Node(node=self.model_node, graph=self.graph)

    def test_init(self):                                                                    # Tests basic initialization
        assert type(self.node)           is MGraph__Node
        assert self.node.node            is self.model_node
        assert self.node.graph           is self.graph
        assert self.node.value         == "test_value"
        assert type(self.node.node_id)  is Random_Guid

    def test__bug__value_operations__type_safe_no_raised(self):                                                        # Tests value getting and setting
        assert self.node.value == "test_value"

        self.node.value = "new_value"
        assert self.node.value == "new_value"

        # with self.assertRaises(TypeError) as context:                                      # Test type validation
        #     self.node.value = 42
        # assert "Value must be of type" in str(context.exception)
        self.node.value = 42        # BUG: should had raised a TypeError

    def test_attribute_operations(self):                                                    # Tests attribute management
        attribute_name  = Safe_Id('test_attr')
        attribute_value = "attr_value"

        # Test adding attribute
        node = self.node.add_attribute(name=attribute_name, value=attribute_value)
        assert node is self.node                                                         # Verify method chaining

        # Verify attribute was added
        attributes = self.node.attributes()
        assert len(attributes) == 1
        attr = attributes[0]
        assert attr.name()  == str(attribute_name)
        assert attr.value() == attribute_value

        # Test retrieving specific attribute
        retrieved_attr = self.node.attribute(attr.id())
        assert retrieved_attr         is not None
        assert retrieved_attr.value() == attribute_value

        # Test retrieving non-existent attribute
        non_existent = self.node.attribute(Random_Guid())
        assert non_existent is None

    def test_adding_attributes_with_different_types(self):                                  # Tests attribute type handling
        test_cases = [("string_attr", "string_value", str  ),
                      ("int_attr",    42,             int  ),
                      ("bool_attr",   True,           bool ),
                      ("float_attr",  3.14,           float)]

        for name, value, expected_type in test_cases:
            attr_name = Safe_Id(name)
            self.node.add_attribute(name=attr_name, value=value, attr_type=expected_type)

            attr = next(a for a in self.node.attributes() if a.name() == name)
            assert attr.value() == value
            assert attr.attribute.data.attribute_type == expected_type