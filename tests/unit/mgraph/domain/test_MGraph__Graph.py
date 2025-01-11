from unittest                                                import TestCase
from mgraph_ai.mgraph.schemas.Schema__MGraph__Default__Types import Schema__MGraph__Default__Types
from osbot_utils.helpers.Safe_Id                             import Safe_Id
from mgraph_ai.mgraph.domain.MGraph__Edge                    import MGraph__Edge
from mgraph_ai.mgraph.domain.MGraph__Node                    import MGraph__Node
from mgraph_ai.mgraph.models.Model__MGraph__Node             import Model__MGraph__Node
from mgraph_ai.mgraph.domain.MGraph__Graph                   import MGraph__Graph
from mgraph_ai.mgraph.models.Model__MGraph__Graph            import Model__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph          import Schema__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph__Config  import Schema__MGraph__Graph__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node           import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute      import Schema__MGraph__Attribute
from osbot_utils.helpers.Random_Guid                         import Random_Guid

class Simple_Node(Schema__MGraph__Node): pass                                                   # Helper class for testing

class test_MGraph__Graph(TestCase):

    def setUp(self):                                                                            # Initialize test data
        self.default_types = Schema__MGraph__Default__Types (node_type     = Simple_Node          ,
                                                             edge_type     = None                 )
        self.graph_config = Schema__MGraph__Graph__Config   (graph_id      = Random_Guid()        )
        self.schema_graph = Schema__MGraph__Graph           (default_types = self.default_types   ,
                                                             nodes         = {}                   ,
                                                             edges         = {}                   ,
                                                             graph_config  = self.graph_config    ,
                                                             graph_type    = Schema__MGraph__Graph)

        self.model_graph = Model__MGraph__Graph             (data=self.schema_graph)                         # Create model graph
        self.graph       = MGraph__Graph                    (model=self.model_graph)

    def test_init(self):                                                                        # Tests basic initialization
        assert type(self.graph)   is MGraph__Graph
        assert self.graph.model   is self.model_graph

    def test_node_operations(self):                                                             # Tests node creation and management

        node = self.graph.new_node(value="test_value")                                          # Create a node

        assert node                 is not None                                                 # Verify node creation
        assert node.value()         == "test_value"
        assert type(node          ) is MGraph__Node
        assert type(node.node     ) is Model__MGraph__Node
        assert type(node.node.data) is Simple_Node

        retrieved_node = self.graph.node(node.node_id())                                             # Retrieve node by ID
        assert retrieved_node         is not None
        assert retrieved_node.value() == "test_value"
        assert type(retrieved_node)   is MGraph__Node

        # List all nodes
        nodes = self.graph.nodes()
        assert len(nodes)       == 1
        assert nodes[0].value() == "test_value"
        assert nodes[0].json()  == retrieved_node.json()

        # Delete node
        assert self.graph.delete_node(node.node_id()) is True
        assert self.graph.node       (node.node_id()) is None

    def test_edge_operations(self):                                                         # Tests edge creation and management
        node1     = self.graph.new_node(value="from_value")                                       # Create nodes for edge
        node2     = self.graph.new_node(value="to_value"  )
        edge      = self.graph.new_edge(from_node_id=node1.node_id(), to_node_id=node2.node_id())                             # Create an edge
        from_node = edge.from_node()
        to_node   = edge.to_node  ()

        assert edge                  is not None                                            # Verify edge creation
        assert from_node.value()     == "from_value"
        assert to_node.value  ()     == "to_value"
        assert type(from_node)       is MGraph__Node
        assert type(to_node  )       is MGraph__Node
        assert type(from_node.graph) is Model__MGraph__Graph
        assert type(to_node  .graph) is Model__MGraph__Graph

        retrieved_edge = self.graph.edge(edge.edge_id())                                             # Retrieve edge by ID
        assert retrieved_edge             is not None
        assert type(retrieved_edge      ) is MGraph__Edge
        assert type(retrieved_edge.graph) is Model__MGraph__Graph


        edges = self.graph.edges()                                                              # List all edges
        assert len(edges)                        == 1
        assert edges[0].json()                   == retrieved_edge.json()

        assert self.graph.delete_edge(edge.edge_id()) is True                                        # Delete edge
        assert self.graph.edge       (edge.edge_id()) is None

    def test_node_with_attributes(self):                                                                        # Test creating nodes with attributes
        attribute_data = { Random_Guid(): Schema__MGraph__Attribute( attribute_id    = Random_Guid()       ,    # Prepare attributes
                                                                     attribute_name  = Safe_Id('test_attr'),
                                                                     attribute_value = "attr_value"        ,
                                                                     attribute_type  = str                )}
        node            = self.graph.new_node(value="test_value", attributes=attribute_data)                          # Create node with attributes

        assert node.attributes()            is not None                                                         # Verify node and attributes
        assert len(node.attributes())       == 1
        assert node.attributes()[0].value() == "attr_value"

    def test_node_with_custom_type(self):                                                   # Test creating nodes with custom types
        class CustomNode(Simple_Node): pass

        node = self.graph.new_node(value="custom_value", node_type=CustomNode)                    # Create node with custom type
        assert node.node.data.node_type is CustomNode
        assert node.value()             == "custom_value"

    def test_graph_state_persistence(self):                                                 # Test graph state persistence
        node1 = self.graph.new_node(value="node1")                                                # Create nodes and edge
        node2 = self.graph.new_node(value="node2")
        edge  = self.graph.new_edge(from_node_id=node1.node_id(), to_node_id=node2.node_id())

        assert type(edge)                         == MGraph__Edge
        assert len(self.graph.nodes())            == 2                                      # Verify multiple graph queries
        assert len(self.graph.edges())            == 1
        assert self.graph.delete_node(node1.node_id()) is True                                   # Delete operations
        assert len(self.graph.nodes())            == 1
        assert len(self.graph.edges())            == 0