from unittest                                           import TestCase

from osbot_utils.utils.Objects import __

from mgraph_ai.mgraph.actions.MGraph__Edit              import MGraph__Edit
from mgraph_ai.mgraph.domain.MGraph__Graph              import MGraph__Graph
from mgraph_ai.mgraph.models.Model__MGraph__Graph       import Model__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph     import Schema__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node      import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute import Schema__MGraph__Attribute
from osbot_utils.helpers.Random_Guid                    import Random_Guid
from osbot_utils.helpers.Safe_Id                        import Safe_Id

class Simple_Node(Schema__MGraph__Node): pass  # Helper class for testing

class test_MGraph__Edit(TestCase):

    def setUp(self):
        schema_graph = Schema__MGraph__Graph(nodes = {}, edges={}, graph_config=None, graph_type=Schema__MGraph__Graph)   # Create a schema graph
        model_graph  = Model__MGraph__Graph (data  = schema_graph)                                                      # Create model and domain graph
        domain_graph = MGraph__Graph        (model = model_graph )
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
        with self.edit as _:
            node_1 = _.new_node("test_node")                                # Create 3x nodes and 2x edges
            node_2 = _.new_node("another_node")
            node_3 = _.new_node("3rd node")
            edge_1 = _.new_edge(node_1.id(), node_2.id())
            edge_2 = _.new_edge(node_2.id(), node_3.id())

            assert _.delete_node(node_1.id()) is True                       # Test node deletion
            assert _.delete_node(node_1.id()) is False
            assert _.graph.node (node_1.id()) is None
            assert _.graph.edge (edge_1.id()) is None

            assert _.delete_edge(edge_2.id()) is True                       # Test edge deletion
            assert _.delete_edge(edge_2.id()) is False
            assert _.graph.edge (edge_2.id()) is None

    def test_node_with_custom_type(self):
        class Custom_Node(Schema__MGraph__Node): pass
        custom_node = Custom_Node()

        assert custom_node.obj() == __(attributes  = __(),
                                       node_config = __(node_id    = custom_node.node_config.node_id,
                                                        value_type = None                          ),
                                       node_type   = 'test_MGraph__Edit.Custom_Node'                ,
                                       value       = None                                           )

        node = self.edit.new_node("custom_value", node_type=Custom_Node)     # Create node with custom type

        assert node.node.data.node_type is Custom_Node
        assert node.value()             == "custom_value"