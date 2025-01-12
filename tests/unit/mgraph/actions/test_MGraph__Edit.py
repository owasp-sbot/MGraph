from unittest                                           import TestCase
from osbot_utils.utils.Misc                             import is_guid
from mgraph_ai.mgraph.domain.MGraph__Node               import MGraph__Node
from osbot_utils.utils.Objects                          import __
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
        self.schema_graph = Schema__MGraph__Graph(nodes = {}, edges={}, graph_config=None, graph_type=Schema__MGraph__Graph)   # Create a schema graph
        self.model_graph  = Model__MGraph__Graph (data  =self.schema_graph)                                                     # Create model and domain graph
        self.domain_graph = MGraph__Graph        (model =self.model_graph )
        self.graph_edit   = MGraph__Edit         (graph =self.domain_graph)                                                     # Create edit object

    def test_add_node(self):
        with self.graph_edit as _:
            node    = _.new_node()
            node_id = node.node_id
            assert type(node)       is MGraph__Node
            assert is_guid(node_id) is True
            assert node.obj()       == __(node=__(data=__(attributes  = __(),
                                                          node_config = __(node_id=node_id,value_type=None),
                                                          node_type   = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Node.Schema__MGraph__Node',
                                                          value       = None  )),
                                          graph=self.model_graph.obj())
            assert node.node.json() == self.model_graph.node(node_id=node_id).json()

            assert _.new_node(value='aaaa').value == 'aaaa'

    def test_new_node(self):
        node = self.graph_edit.new_node(value="test_value")                                                                         # Create a simple node
        assert node         is not None
        assert node.value == "test_value"

    def test_new_node_with_attributes(self):
        attribute = Schema__MGraph__Attribute(attribute_id    = Random_Guid()       ,                                   # Create attribute
                                              attribute_name  = Safe_Id('test_attr'),
                                              attribute_value = "attr_value"        ,
                                              attribute_type  = str                 )
        node      = self.graph_edit.new_node(value="test_value", attributes={attribute.attribute_id: attribute})                     # Create node with attributes

        assert node                         is not None
        assert len(node.attributes())       == 1
        assert node.attributes()[0].value() == "attr_value"

    def test_new_edge(self):
        node1 = self.graph_edit.new_node(value="node1")                                                                             # Create two nodes
        node2 = self.graph_edit.new_node(value="node2")
        edge  = self.graph_edit.new_edge(from_node_id=node1.node_id, to_node_id=node2.node_id)                                                              # Create edge between nodes

        assert edge is not None
        assert edge.from_node().value == "node1"
        assert edge.to_node  ().value == "node2"

    def test_deletion(self):
        with self.graph_edit as _:
            node_1 = _.new_node(value="test_node"   )                                # Create 3x nodes and 2x edges
            node_2 = _.new_node(value="another_node")
            node_3 = _.new_node(value="3rd node"    )
            edge_1 = _.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            edge_2 = _.new_edge(from_node_id=node_2.node_id, to_node_id=node_3.node_id)

            assert _.delete_node(node_1.node_id) is True                       # Test node deletion
            assert _.delete_node(node_1.node_id) is False
            assert _.graph.node (node_1.node_id) is None
            assert _.graph.edge (edge_1.edge_id) is None

            assert _.delete_edge(edge_2.edge_id) is True                       # Test edge deletion
            assert _.delete_edge(edge_2.edge_id) is False
            assert _.graph.edge (edge_2.edge_id) is None

    def test_node_with_custom_type(self):
        class Custom_Node(Schema__MGraph__Node): pass
        custom_node = Custom_Node()

        assert custom_node.obj() == __(attributes  = __(),
                                       node_config = __(node_id    = custom_node.node_config.node_id,
                                                        value_type = None                          ),
                                       node_type   = 'test_MGraph__Edit.Custom_Node'                ,
                                       value       = None                                           )

        node = self.graph_edit.new_node(value="custom_value", node_type=Custom_Node)     # Create node with custom type

        assert node.node.data.node_type is Custom_Node
        assert node.value             == "custom_value"