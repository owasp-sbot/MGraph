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
        mgraph = self.new_graph()
        if x >0  and y > 0 :
            for i in range(x):
                mgraph.new_node()
            nodes_ids = mgraph.data().nodes_ids()
            for i in range(y):
                from_node_id = nodes_ids[random_int(max=x) - 1]         # get the node_id of a random 'from node'
                to_node_id   = nodes_ids[random_int(max=x) - 1]         # get the node_id of a random 'to node'
                # from_node    = mgraph.nodes[from_node_id]
                # to_node      = mgraph.nodes[to_node_id  ]
                mgraph.add_edge(from_node_id=from_node_id, to_node_id=to_node_id)

        return mgraph