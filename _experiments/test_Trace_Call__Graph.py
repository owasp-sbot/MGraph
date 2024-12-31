from unittest import TestCase

import pytest

from osbot_utils.graphs.mgraph.MGraphs import MGraphs
from osbot_utils.utils.Files import file_exists, file_delete
from osbot_utils.helpers.trace.Trace_Call__Graph import Trace_Call__Graph


class test_Trace_Call__Graph(TestCase):

    def setUp(self):
        self.trace_graph  = Trace_Call__Graph()
        self.trace_config = self.trace_graph.config

    @pytest.mark.skip("Fix this when Trace_Call__Graph is reimplemented with new version of Mermaid Graph")
    def test_create(self):
        self.trace_config.capture(contains=['osbot']).print_on_exit(False )

        with self.trace_graph as _:

            MGraphs().new__random(x_nodes=4,y_edges=4)

            # with Temp_File() as temp_file:
            #     temp_file.write('test')
            #     assert file_exists(temp_file.path())
            #     str_md5('aaaa')
            #     pass

        mermaid_graph = self.trace_graph.create()
        #mermaid_graph.print()
        #mermaid_graph.print_code()
        target_file = '/tmp/mermaid.md'
        file_delete(target_file)
        mermaid_graph.save()
        assert file_exists(target_file)
        #pprint(_.trace_call_handler.traces())

