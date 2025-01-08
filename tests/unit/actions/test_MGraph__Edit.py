from unittest                                       import TestCase
from mgraph_ai.actions.MGraph__Edit                 import MGraph__Edit
from mgraph_ai.domain.MGraph__Graph                 import MGraph__Graph
from mgraph_ai.models.Model__MGraph__Graph          import Model__MGraph__Graph
from mgraph_ai.schemas.Schema__MGraph__Graph        import Schema__MGraph__Graph
from mgraph_ai.schemas.Schema__MGraph__Node         import Schema__MGraph__Node
from mgraph_ai.schemas.Schema__MGraph__Attribute    import Schema__MGraph__Attribute
from osbot_utils.helpers.Random_Guid                import Random_Guid
from osbot_utils.helpers.Safe_Id                    import Safe_Id

class Simple_Node(Schema__MGraph__Node): pass  # Helper class for testing

class test_MGraph__Edit(TestCase):
    def setUp(self):
        schema_graph = Schema__MGraph__Graph(nodes = {}, edges={}, graph_config=None, graph_type=Schema__MGraph__Graph)   # Create a schema graph
        model_graph  = Model__MGraph__Graph (data  = schema_graph)                                                      # Create model and domain graph
        domain_graph = MGraph__Graph        (graph = model_graph )
        self.edit    = MGraph__Edit         (graph = domain_graph)                                                      # Create edit object

    def test_new_node(self):
        node = self.edit.new_node("test_value")                                                                         # Create a simple node
        assert node         is not None
        assert node.value() == "test_value"

    def test_new_node_with_attributes(self):
        attribute = Schema__MGraph__Attribute(attribute_id    = Random_Guid()       ,                                   # Create attribute
                                              attribute_name  = Safe_Id('test_attr'),
                                              attribute_value = "attr_value"        ,
                                              attribute_type  = str                 )
        node      = self.edit.new_node("test_value",attributes={attribute.attribute_id: attribute})                     # Create node with attributes

        assert node                         is not None
        assert len(node.attributes())       == 1
        assert node.attributes()[0].value() == "attr_value"

    def test_new_edge(self):
        node1 = self.edit.new_node("node1")                                                                             # Create two nodes
        node2 = self.edit.new_node("node2")
        edge  = self.edit.new_edge(node1.id(), node2.id())                                                              # Create edge between nodes

        assert edge is not None
        assert edge.from_node().value() == "node1"
        assert edge.to_node().value() == "node2"

    def test_deletion(self):
        # Create a node and an edge
        node = self.edit.new_node("test_node")
        node2 = self.edit.new_node("another_node")
        edge = self.edit.new_edge(node.id(), node2.id())

        # Test node deletion
        assert self.edit.delete_node(node.id()) is True
        assert self.edit.graph.node(node.id()) is None

        # Test edge deletion
        assert self.edit.delete_edge(edge.id()) is True
        assert self.edit.graph.edge(edge.id()) is None

    def test_node_with_custom_type(self):
        class CustomNode(Schema__MGraph__Node): pass

        # Create node with custom type
        node = self.edit.new_node("custom_value", node_type=CustomNode)

        assert node.node.data.node_type is CustomNode
        assert node.value() == "custom_value"