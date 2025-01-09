from mgraph_ai.providers.mermaid.domain.Mermaid__Graph  import Mermaid__Graph
from osbot_utils.helpers.trace.Trace_Call               import Trace_Call

# todo: reimplement this class when Mermaid__Graph has been updated to new version
class Trace_Call__Graph(Trace_Call):

    def create(self):
        mermaid_graph = Mermaid__Graph()
        self.trace_call_handler.stack.root_node.func_name = 'trace_root'
        for trace in self.trace_call_handler.traces():
            node_key   = trace.func_name
            class_name = trace.module.split('.')[-1]
            node_label = f'`**{trace.func_name}**\n*{class_name}*`'
            mermaid_graph.add_node(key=node_key, label=node_label)

        nodes__by_key = mermaid_graph.data().nodes__by_id()

        for trace in self.trace_call_handler.traces():
            from_node = nodes__by_key[trace.func_name]
            for child in trace.children:
                to_node = nodes__by_key[child.func_name]
                mermaid_graph.add_edge(from_node=from_node, to_node=to_node)
        return mermaid_graph