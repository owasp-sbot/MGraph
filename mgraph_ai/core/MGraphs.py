from mgraph_ai.core.MGraph__Random_Graphs import MGraph__Random_Graphs

class MGraphs:

    def new__random(self, config=None, graph_key=None, x_nodes=10, y_edges=20):
        return MGraph__Random_Graphs(config=config, graph_key=graph_key).with_x_nodes_and_y_edges(x=x_nodes, y=y_edges)

    # todo : implement based on multiple save a load methods
    # def load(self, file_path):
    #     if file_exists(file_path):
    #         if file_extension(file_path):
    #             return pickle_load_from_file(file_path)