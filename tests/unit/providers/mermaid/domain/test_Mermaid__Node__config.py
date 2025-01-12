from unittest                                                         import TestCase
from mgraph_ai.providers.mermaid.domain.Domain__Mermaid__Node                 import Domain__Mermaid__Node
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Shape import Schema__Mermaid__Node__Shape
from mgraph_ai.providers.mermaid.utils.Test_Data__Mermaid             import Test_Data_Mermaid


class test_Mermaid__Node__config(TestCase):     # todo: refactor these tests to the correct location since most are related to the node's .node_config

    def setUp(self):
        test_data        = Test_Data_Mermaid.create_test_graph(num_nodes=1)
        self.graph_model = test_data['graph_model']
        self.nodes       = test_data['nodes']
        self.first_node = Domain__Mermaid__Node(node=self.nodes[0], graph=self.graph_model)

    def test_init(self):
        assert isinstance(self.first_node, Domain__Mermaid__Node)
        assert self.first_node.value == "value_key_0"

    def test_markdown(self):
        assert self.first_node.node_config.markdown is False
        self.first_node.markdown(True)
        assert self.first_node.node_config.markdown is True
        self.first_node.markdown(False)
        assert self.first_node.node_config.markdown is False

    def test_wrap_with_quotes(self):
        assert self.first_node.node_config.wrap_with_quotes is True
        self.first_node.wrap_with_quotes(False)
        assert self.first_node.node_config.wrap_with_quotes is False
        self.first_node.wrap_with_quotes(True)
        assert self.first_node.node_config.wrap_with_quotes is True

    def test_show_label(self):
        assert self.first_node.node_config.show_label is True
        self.first_node.show_label(False)
        assert self.first_node.node_config.show_label is False
        self.first_node.show_label(True)
        assert self.first_node.node_config.show_label is True

    def test_shape_methods(self):
        # Test generic shape setter
        self.first_node.shape('circle')
        assert self.first_node.node_config.node_shape == Schema__Mermaid__Node__Shape.circle

        # Test all specific shape methods
        shape_methods = [
            ('shape_asymmetric', Schema__Mermaid__Node__Shape.asymmetric),
            ('shape_circle', Schema__Mermaid__Node__Shape.circle),
            ('shape_cylindrical', Schema__Mermaid__Node__Shape.cylindrical),
            ('shape_default', Schema__Mermaid__Node__Shape.default),
            ('shape_double_circle', Schema__Mermaid__Node__Shape.double_circle),
            ('shape_hexagon', Schema__Mermaid__Node__Shape.hexagon),
            ('shape_parallelogram', Schema__Mermaid__Node__Shape.parallelogram),
            ('shape_parallelogram_alt', Schema__Mermaid__Node__Shape.parallelogram_alt),
            ('shape_stadium', Schema__Mermaid__Node__Shape.stadium),
            ('shape_subroutine', Schema__Mermaid__Node__Shape.subroutine),
            ('shape_rectangle', Schema__Mermaid__Node__Shape.rectangle),
            ('shape_rhombus', Schema__Mermaid__Node__Shape.rhombus),
            ('shape_round_edges', Schema__Mermaid__Node__Shape.round_edges),
            ('shape_trapezoid', Schema__Mermaid__Node__Shape.trapezoid),
            ('shape_trapezoid_alt', Schema__Mermaid__Node__Shape.trapezoid_alt)
        ]

        for method_name, expected_shape in shape_methods:
            method = getattr(self.first_node, method_name)
            result = method()
            assert result is self.first_node  # Test method chaining
            assert self.first_node.node_config.node_shape == expected_shape

    def test_shape_invalid(self):
        # Test with invalid shape name
        self.first_node.shape('invalid_shape')
        assert self.first_node.node_config.node_shape == Schema__Mermaid__Node__Shape.default

        # Test with None
        self.first_node.shape(None)
        assert self.first_node.node_config.node_shape == Schema__Mermaid__Node__Shape.default