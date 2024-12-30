from typing                             import List
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.utils.Misc             import random_text, lower
from mgraph_ai.core.MGraph__Config      import MGraph__Config
from mgraph_ai.core.MGraph__Edge        import MGraph__Edge
from mgraph_ai.core.MGraph__Node        import MGraph__Node


# todo add support for storing the data in sqlite so that we get the ability to search nodes and edges
class MGraph(Type_Safe):
    config : MGraph__Config
    edges  : List[MGraph__Edge]
    key    : str
    nodes  : List[MGraph__Node]


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.key:
            self.key = random_text("mgraph", lowercase=True)                 # make sure there is always a key

    def add_edge(self, from_node, to_node, label=None,attributes=None):
        if self.config.allow_circle_edges is False:
            if from_node == to_node:
                return None
        if self.config.allow_duplicate_edges is False:                          # todo: figure out if there is a more efficient way to do this
            for edge in self.edges:
                if edge.from_node == from_node and edge.to_node == to_node:
                    return None
        new_edge = MGraph__Edge(from_node=from_node, to_node=to_node, label=label, attributes=attributes)
        self.edges.append(new_edge)
        return new_edge

    def add_node(self, key=None, label=None, attributes=None):
        new_node = MGraph__Node(key=key, label=label, attributes=attributes)
        self.nodes.append(new_node)
        return new_node

    def data(self):
        from mgraph_ai.core.MGraph__Data import MGraph__Data
        return MGraph__Data(mgraph=self)

    # def save(self, format='pickle'):
    #     if format == 'pickle':
    #         return pickle_save_to_file(self)

    #todo: add save that return saved object
    # def save(self):
    #     from mgraph_ai.core.MGraph__Serializer import MGraph__Serializer        # due to circular dependency
    #     return MGraph__Serializer(mgraph=self).save()

    def print(self):
        print()
        return self.data().print()