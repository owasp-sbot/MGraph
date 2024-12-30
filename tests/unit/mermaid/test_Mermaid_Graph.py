import sys
from unittest import TestCase

import pytest

from osbot_utils.base_classes.Kwargs_To_Self        import Kwargs_To_Self
from osbot_utils.utils.Misc                         import list_set
from osbot_utils.utils.Objects                      import base_classes, base_types
from mgraph_ai.core.MGraph               import MGraph
from mgraph_ai.core.MGraphs              import MGraphs
from mgraph_ai.mermaid.Mermaid__Graph      import Mermaid__Graph


class test_Mermaid_MGraph(TestCase):

    def setUp(self):
        self.mgraph        = MGraphs().new__random(x_nodes=4,y_edges=4)
        self.mermaid_graph = Mermaid__Graph()#.cast(self.mgraph)


    def test__init__(self):
        assert type(self.mermaid_graph) is Mermaid__Graph
        assert base_types(self.mermaid_graph) == [MGraph, Kwargs_To_Self, object]
        assert list_set(self.mermaid_graph.__locals__()) == ['config', 'edges', 'key', 'mermaid_code', 'nodes']
        # assert hasattr(self.mermaid_graph, "convert_nodes") is True
        # assert hasattr(self.mgraph       , "convert_nodes") is False

    # def test_code(self):
    #     with Stdout() as stdout:
    #         with self.mermaid_graph as _:
    #             print(_.code())
    #     assert stdout.value() == '\n'.join(self.mermaid_graph.mermaid_code) + '\n'
    #
    # def test_code_markdown(self):
    #     code_markdown = self.mermaid_graph.code_markdown()
    #     assert code_markdown == '\n'.join(['# Mermaid Graph'                 ,
    #                                        "```mermaid"                      ,
    #                                        *self.mermaid_graph.mermaid_code ,
    #                                        "```"                             ])
    #
    #
    # def test_convert_nodes(self):
    #     assert len(self.mermaid_graph.nodes) == len(self.mgraph.nodes)
    #     assert len(self.mermaid_graph.edges  ) == len(self.mgraph.edges)
    #
    #     for node in self.mgraph.nodes:
    #         assert type(node) is Mermaid__Node
    #
    #     for node in self.mermaid_graph.nodes:
    #         assert type(node) is Mermaid__Node
    #
    #
    #
    #     with patch('builtins.print') as _:          # comparing print outputs using mock patch technique
    #         self.mgraph       .print()
    #         self.mermaid_graph.print()
    #
    #     print_calls   = int(_.call_count / 2)
    #     mgraph_calls  = _.call_args_list[:print_calls]
    #     mermaid_calls = _.call_args_list[print_calls:]
    #     assert len(mgraph_calls) == len(mermaid_calls)
    #     assert mgraph_calls      == mermaid_calls
    #
    #     # comparing print outputs using redirect_stdout technique
    #     output_mgraph = io.StringIO()
    #     with redirect_stdout(output_mgraph):
    #         self.mgraph.print()
    #
    #     output_mermaid = io.StringIO()
    #     with redirect_stdout(output_mermaid):
    #         self.mermaid_graph.print()
    #     assert output_mgraph.getvalue() == output_mermaid.getvalue()
    #
    # def test_edges(self):
    #     for edge in self.mermaid_graph.edges:
    #         assert type(edge) is Mermaid__Edge
    #
    # def test_nodes(self):
    #     for node in self.mermaid_graph.nodes:
    #         assert type(node) is Mermaid__Node
    #
    # def test_save(self):
    #     with Temp_File() as temp_file:
    #         file_path = temp_file.path()
    #         assert self.mermaid_graph.save(file_path) == file_path
    #         assert file_contents(file_path) == self.mermaid_graph.code_markdown()

        #self.mermaid_graph.save('/tmp/mermaid.md')