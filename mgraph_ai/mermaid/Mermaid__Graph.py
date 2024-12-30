from typing                             import List
from mgraph_ai.mermaid.Mermaid__Edge    import Mermaid__Edge
from mgraph_ai.mermaid.Mermaid__Node    import Mermaid__Node
from mgraph_ai.core.MGraph              import MGraph


class Mermaid__Graph(MGraph):
    edges        : List[Mermaid__Edge]
    mermaid_code : List
    nodes        : List[Mermaid__Node]

    # def __init__(self, mgraph=None):
    #     super().__init__()
    #     if mgraph is None:
    #         mgraph = MGraph()
    #     self.__dict__ = mgraph.__dict__
    #     self.convert_nodes().convert_edges()

    # def cast(self, source):
    #     self.__dict__ = source.__dict__
    #     return self

    # def add_edge(self, **kwargs):
    #     #new_edge = super().add_edge(*args, **kwargs)
    #     mermaid_edge = Mermaid__Edge(**kwargs)
    #     self.edges.append(mermaid_edge)
    #     return mermaid_edge
    #
    def add_node(self, **kwargs):
        mermaid_node = Mermaid__Node(**kwargs)
        self.nodes.append(mermaid_node)
        return mermaid_node

    #
    #
    # def add_line(self, line):
    #     self.mermaid_code.append(line)
    #     return line
    #
    # def code(self):
    #     self.code_create()
    #     return '\n'.join(self.mermaid_code)
    #
    # def code_create(self):
    #     with self as _:
    #         _.reset_code()
    #         _.add_line('graph LR')
    #         for node in _.nodes:
    #             _.add_line(node.code())
    #         _.add_line('')
    #         for edge in _.edges:
    #             _.add_line(edge.code())
    #     return self
    #
    # def code_markdown(self):
    #     self.code_create()
    #     markdown = ['# Mermaid Graph',
    #                 "```mermaid" ,
    #                 *self.mermaid_code,
    #                 "```"]
    #
    #     return '\n'.join(markdown)
    #
    # def convert_edges(self):
    #     new_edges = []
    #     for edge in self.edges:
    #         new_edges.append(Mermaid__Edge().cast(edge))
    #     self.edges = new_edges
    #     return self
    #
    # def convert_nodes(self):
    #     new_nodes = []
    #     for node in self.nodes:
    #         mermaid_node = Mermaid__Node().cast(node)
    #         new_nodes.append(mermaid_node)
    #     self.nodes = new_nodes
    #     return self
    #
    # def reset_code(self):
    #     self.mermaid_code = []
    #     return self
    #
    # def save(self, target_file=None):
    #     file_path = target_file or '/tmp/mermaid.md'
    #
    #     with open(file_path, 'w') as file:
    #         file.write(self.code_markdown())
    #     return file_path
    #
    # def print_code(self):
    #     print(self.code())