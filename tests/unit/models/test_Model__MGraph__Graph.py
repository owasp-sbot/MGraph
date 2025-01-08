from unittest                                       import TestCase
from mgraph_ai.schemas.Schema__MGraph__Attribute    import Schema__MGraph__Attribute
from osbot_utils.helpers.Safe_Id                    import Safe_Id
from mgraph_ai.models.Model__MGraph__Graph          import Model__MGraph__Graph
from mgraph_ai.schemas.Schema__MGraph__Graph        import Schema__MGraph__Graph
from mgraph_ai.schemas.Schema__MGraph__Graph_Config import Schema__MGraph__Graph_Config
from mgraph_ai.schemas.Schema__MGraph__Node         import Schema__MGraph__Node
from mgraph_ai.schemas.Schema__MGraph__Edge         import Schema__MGraph__Edge
from osbot_utils.helpers.Random_Guid                import Random_Guid

class Simple_Node(Schema__MGraph__Node): pass                                               # Helper class for testing

class test_Model__MGraph__Graph(TestCase):

    def setUp(self):                                                                        # Initialize test data
        self.graph_config = Schema__MGraph__Graph_Config(graph_id          = Random_Guid()         ,
                                                         default_node_type = Simple_Node           ,
                                                         default_edge_type = Schema__MGraph__Edge  )
        self.graph = Schema__MGraph__Graph              (edges             = {}                    ,
                                                         nodes             = {}                    ,
                                                         graph_config      = self.graph_config     ,
                                                         graph_type        = Schema__MGraph__Graph )
        self.model = Model__MGraph__Graph(data=self.graph)

    def test_init(self):                                                                    # Tests basic initialization
        assert type(self.model)              is Model__MGraph__Graph
        assert self.model.data               is self.graph
        assert len(self.model.data.nodes)    == 0
        assert len(self.model.data.edges)    == 0

    def test_node_operations(self):                                                         # Tests node creation, addition, and removal
        node = self.model.new_node("test_value")                                            # Test node creation
        assert isinstance(node, Schema__MGraph__Node)
        assert node.value                         == "test_value"
        assert type(node.node_config.value_type)  is type(str)
        assert node.node_config.node_id           in self.model.data.nodes

        retrieved = self.model.node(node.node_config.node_id)                           # Test node retrieval
        assert retrieved == node

        assert self.model.delete_node(node.node_config.node_id) is True                     # Test node removal
        assert node.node_config.node_id                     not in self.model.data.nodes

        assert self.model.delete_node(Random_Guid()) is False                    # Test removing non-existent node

    def test_edge_operations(self):                                                         # Tests edge creation, addition, and removal
        node1 = self.model.new_node("node1")                                                # Create two nodes
        node2 = self.model.new_node("node2")

        edge = self.model.new_edge(node1.node_config.node_id, node2.node_config.node_id)    # Test edge creation
        assert isinstance(edge, Schema__MGraph__Edge)   is True
        assert edge.from_node_id                        == node1.node_config.node_id
        assert edge.to_node_id                          == node2.node_config.node_id

        retrieved = self.model.get_edge(edge.edge_config.edge_id)                           # Test edge retrieval
        assert retrieved == edge

        assert self.model.delete_edge(edge.edge_config.edge_id) is True                     # Test edge removal
        assert edge.edge_config.edge_id not in self.model.data.edges

        assert self.model.delete_edge(Random_Guid()) is False                               # Test removing non-existent edge

    def test_node_removal_cascades_to_edges(self):                                          # Tests that removing a node removes connected edges
        node1 = self.model.new_node("node1")
        node2 = self.model.new_node("node2")
        node3 = self.model.new_node("node3")

        edge1 = self.model.new_edge(node1.node_config.node_id, node2.node_config.node_id)   # Create edges
        edge2 = self.model.new_edge(node2.node_config.node_id, node3.node_config.node_id)

        assert len(self.model.data.edges) == 2                                              # Verify initial state

        self.model.delete_node(node2.node_config.node_id)                                   # Remove node2 (should remove both edges)

        assert len(self.model.data.edges) == 0                                              # Verify edges were removed
        assert edge1.edge_config.edge_id not in self.model.data.edges
        assert edge2.edge_config.edge_id not in self.model.data.edges

    def test_edge_validation(self):                                                         # Tests edge validation
        with self.assertRaises(ValueError) as context:                                      # Test creating edge with non-existent nodes
            self.model.new_edge(Random_Guid(), Random_Guid())
        assert "Node" in str(context.exception)

    def test_custom_node_types(self):                                                       # Tests creation of nodes with custom types
        class Custom_Node(Schema__MGraph__Node): pass

        default_node = self.model.new_node("default_value")                                 # Create node with default type
        assert isinstance(default_node, Schema__MGraph__Node)
        assert default_node.node_type == Simple_Node                                        # Should use default_node_type

        custom_node = self.model.new_node("custom_value", node_type=Custom_Node)            # Create node with custom type
        assert isinstance(custom_node, Schema__MGraph__Node)
        assert custom_node.node_type == Custom_Node

    def test_graph_queries(self):                                                           # Tests graph querying methods
        node1 = self.model.new_node("node1")                                                # Add some test nodes
        node2 = self.model.new_node("node2")
        node3 = self.model.new_node("node3")

        nodes = list(self.model.nodes())                                                    # Test nodes() method
        assert len(nodes) == 3
        assert node1 in nodes
        assert node2 in nodes
        assert node3 in nodes

        graph = self.model.graph()                                                          # Test graph() method
        assert isinstance(graph, Schema__MGraph__Graph)
        assert len(graph.nodes) == 3
        assert len(graph.edges) == 0

    def test_node_attributes(self):                                                                 # Tests node creation with attributes
        attribute = Schema__MGraph__Attribute(attribute_id    = Random_Guid()       ,               # Create attribute
                                              attribute_name  = Safe_Id('test_attr'),
                                              attribute_value = "attr_value"        ,
                                              attribute_type  = str                 )

        node = self.model.new_node("test_value", attributes={attribute.attribute_id: attribute})    # Create node with attribute
        assert len(node.attributes) == 1
        assert node.attributes[attribute.attribute_id] == attribute

    def test_edge_constraints(self):                                                        # Tests edge creation constraints
        class Another_Node(Schema__MGraph__Node): pass                                      # Create nodes of different types
        
        node1 = self.model.new_node("node1", node_type=Simple_Node)
        node2 = self.model.new_node("node2", node_type=Another_Node)

        edge = self.model.new_edge(node1.node_config.node_id, node2.node_config.node_id)    # Create edge between nodes

        assert edge.edge_config.from_node_type == Simple_Node                               # Verify edge node types
        assert edge.edge_config.to_node_type   == Another_Node

        self.model.delete_node(node1.node_config.node_id)                                   # Test edge validation with deleted node
        with self.assertRaises(ValueError) as context:
            self.model.add_edge(edge)
        assert "Source node" in str(context.exception)