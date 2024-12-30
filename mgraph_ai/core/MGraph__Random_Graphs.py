from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.utils.Misc             import random_int
from mgraph_ai.core.MGraph              import MGraph
from mgraph_ai.core.MGraph__Config      import MGraph__Config

class MGraph__Random_Graphs(Type_Safe):
    config     : MGraph__Config
    graph_key : str

    def new_graph(self):
        return MGraph(config=self.config, key=self.graph_key)

    def with_x_nodes_and_y_edges(self, x=10, y=20):
        MGraph = self.new_graph()
        if x >0  and y > 0 :
            for i in range(x):
                MGraph.add_node()
            for i in range(y):
                from_node_id = random_int(max=x) - 1
                to_node_id   = random_int(max=x) - 1
                from_node    = MGraph.nodes[from_node_id]
                to_node      = MGraph.nodes[to_node_id  ]
                MGraph.add_edge(from_node=from_node, to_node=to_node)

        return MGraph