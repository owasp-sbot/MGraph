import sys
from unittest import TestCase

import pytest

from mgraph_ai.mermaid.Mermaid import Mermaid
from mgraph_ai.mermaid.Mermaid__Node import Mermaid__Node
from osbot_utils.utils.Misc import list_set

from mgraph_ai.mermaid.Mermaid__Edge import Mermaid__Edge


class test_Mermaid_Edge(TestCase):

    def setUp(self):
        self.mermaid_edge = Mermaid__Edge()

    def test__init__(self):
        assert type(self.mermaid_edge) is Mermaid__Edge
        assert list_set(self.mermaid_edge.__dict__) == ['attributes', 'config', 'from_node', 'label', 'to_node']

    def test_render_edge(self):
        from_node = self.mermaid_edge.from_node
        to_node   = self.mermaid_edge.to_node
        assert self.mermaid_edge.render_edge() == f'    {from_node.key} --> {to_node.key}'
        from_node.label = 'from node'
        to_node.label   = 'to node'
        assert self.mermaid_edge.render_edge() == f'    {from_node.key} --> {to_node.key}'
        self.mermaid_edge.label = 'link_type'
        assert self.mermaid_edge.render_edge() == f'    {from_node.key} --"{self.mermaid_edge.label}"--> {to_node.key}'
        self.mermaid_edge.edge_mode__lr_using_pipe()
        assert self.mermaid_edge.render_edge() == f'    {from_node.key} -->|{self.mermaid_edge.label}| {to_node.key}'
        self.mermaid_edge.output_node_to()
        assert self.mermaid_edge.render_edge() == f'    {from_node.key} -->|{self.mermaid_edge.label}| {to_node.key}["to node"]'


    def test_convert_nodes(self):
        assert type(self.mermaid_edge.from_node) is Mermaid__Node
        assert type(self.mermaid_edge.to_node  ) is Mermaid__Node

    def test__config__edge__output_node_from(self):
        with Mermaid() as _:
            new_edge = _.add_edge('id', 'id2').output_node_from()
            assert _.code()               == 'graph LR\n    id["id"]\n    id2["id2"]\n\n    id["id"] --> id2'
            assert new_edge.config.output_node_from is True
            assert new_edge.render_edge() == '    id["id"] --> id2'
            new_edge.output_node_from(False)
            assert new_edge.config.output_node_from is False
            assert new_edge.render_edge() == '    id --> id2'