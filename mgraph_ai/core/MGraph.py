from typing                             import List, Dict
from osbot_utils.helpers.Random_Guid    import Random_Guid
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
    nodes  : Dict[Random_Guid, MGraph__Node]


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.key:
            self.key = random_text("mgraph", lowercase=True)                 # make sure there is always a key

    def add_edge(self, from_node_id, to_node_id, attributes=None):
        if self.config.allow_circle_edges is False:
            if from_node_id == to_node_id:
                return None
        if self.config.allow_duplicate_edges is False:                          # todo: figure out if there is a more efficient way to do this
            for edge in self.edges:
                if edge.from_node_id == from_node_id and edge.to_node_id == to_node_id:
                    return None
        new_edge = MGraph__Edge(from_node_id=from_node_id, to_node_id=to_node_id, attributes=attributes)
        self.edges.append(new_edge)
        return new_edge

    def add_node(self, new_node: MGraph__Node):
        self.nodes[new_node.node_id] = new_node
        return new_node


    # def data(self):
    #     from mgraph_ai.core.MGraph__Data import MGraph__Data
    #     return MGraph__Data(graph=self.graph)

    def node(self, node_id):
        return self.nodes.get(node_id)

    # def save(self, format='pickle'):
    #     if format == 'pickle':
    #         return pickle_save_to_file(self)

    #todo: add save that return saved object
    # def save(self):
    #     from mgraph_ai.core.MGraph__Serializer import MGraph__Serializer        # due to circular dependency
    #     return MGraph__Serializer(mgraph=self).save()

    # def print(self):
    #     print()
    #     return self.data().print()

    def new_node(self, attributes=None):
        new_node = MGraph__Node(attributes=attributes)
        self.nodes[new_node.node_id] = new_node
        return new_node