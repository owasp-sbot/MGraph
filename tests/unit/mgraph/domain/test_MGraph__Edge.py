from unittest                                              import TestCase
from osbot_utils.helpers.Safe_Id                           import Safe_Id
from mgraph_ai.mgraph.domain.MGraph__Edge                  import MGraph__Edge
from mgraph_ai.mgraph.models.Model__MGraph__Edge           import Model__MGraph__Edge
from mgraph_ai.mgraph.models.Model__MGraph__Graph          import Model__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge         import Schema__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph        import Schema__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node         import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config import Schema__MGraph__Edge__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Config import Schema__MGraph__Node__Config
from osbot_utils.helpers.Random_Guid                       import Random_Guid

class test_MGraph__Edge(TestCase):

    def setUp(self):                                                                        # Initialize test data
        self.graph = Model__MGraph__Graph(data=None)                                        # Mock graph for testing


        self.from_node_config = Schema__MGraph__Node__Config(node_id    = Random_Guid(),  # Create source and target nodes
                                                             value_type = str)
        self.from_schema_node  = Schema__MGraph__Node      (attributes  = {}                    ,
                                                            node_config = self.from_node_config,
                                                            node_type   = Schema__MGraph__Node  ,
                                                            value       = "from_value"          )
        self.to_node_config = Schema__MGraph__Node__Config  (node_id    = Random_Guid(),
                                                             value_type = str)
        self.to_schema_node = Schema__MGraph__Node         (attributes  = {}                  ,
                                                            node_config = self.to_node_config,
                                                            node_type   = Schema__MGraph__Node,
                                                            value       = "to_value"          )

        # Add nodes to the graph
        self.graph.data = Schema__MGraph__Graph(nodes        = { self.from_schema_node.node_config.node_id: self.from_schema_node,
                                                                 self.to_schema_node.node_config.node_id  : self.to_schema_node  },
                                                edges        = {}                                                                 ,
                                                graph_config = None                                                               ,
                                                graph_type   = Schema__MGraph__Graph                                              )

        # Create edge configuration and schema
        self.edge_config = Schema__MGraph__Edge__Config(edge_id        = Random_Guid(),
                                                        from_node_type = Schema__MGraph__Node,
                                                        to_node_type   = Schema__MGraph__Node)
        self.schema_edge = Schema__MGraph__Edge       (attributes     = {}                   ,
                                                       edge_config    = self.edge_config     ,
                                                       edge_type      = Schema__MGraph__Edge ,
                                                       from_node_id   = self.from_schema_node.node_config.node_id,
                                                       to_node_id     = self.to_schema_node.node_config.node_id)

        # Create model and domain edge
        self.model_edge = Model__MGraph__Edge(data=self.schema_edge)
        self.edge       = MGraph__Edge(edge=self.model_edge, graph=self.graph)

    def test_init(self):                                                                    # Tests basic initialization
        assert type(self.edge)      is MGraph__Edge
        assert self.edge.edge       is self.model_edge
        assert self.edge.graph      is self.graph
        assert type(self.edge.id()) is Random_Guid

    def test_node_operations(self):                                                         # Tests from_node and to_node methods
        from_node = self.edge.from_node()
        to_node   = self.edge.to_node()

        assert from_node         is not None
        assert to_node           is not None
        assert from_node.value() == "from_value"
        assert to_node.value  () == "to_value"

    def test_attribute_operations(self):                                                    # Tests attribute management
        attribute_name  = Safe_Id('test_attr')
        attribute_value = "attr_value"

        edge = self.edge.add_attribute(name=attribute_name, value=attribute_value)          # Test adding attribute
        assert edge is self.edge                                                            # Verify method chaining

        attributes = self.edge.attributes()                                                 # Verify attribute was added
        attr       = attributes[0]
        assert len(attributes) == 1
        assert attr.name()     == str(attribute_name)
        assert attr.value()    == attribute_value

        retrieved_attr = self.edge.attribute(attr.id())                                     # Test retrieving specific attribute
        assert retrieved_attr         is not None
        assert retrieved_attr.value() == attribute_value

        non_existent = self.edge.attribute(Random_Guid())                                   # Test retrieving non-existent attribute
        assert non_existent is None

    def test_adding_attributes_with_different_types(self):                                  # Tests attribute type handling
        test_cases = [("string_attr", "string_value", str  ),
                      ("int_attr",    42,             int  ),
                      ("bool_attr",   True,           bool ),
                      ("float_attr",  3.14,           float)]

        for name, value, expected_type in test_cases:
            attr_name = Safe_Id(name)
            self.edge.add_attribute(name=attr_name, value=value, attr_type=expected_type)

            attr = next(a for a in self.edge.attributes() if a.name() == name)
            assert attr.value()                       == value
            assert attr.attribute.data.attribute_type == expected_type