from typing                                                   import Dict

from mgraph_ai.mermaid.models.Model__Mermaid__Node import Model__Mermaid__Node
from mgraph_ai.mermaid.schemas.Schema__Mermaid__Graph__Config import Schema__Mermaid__Graph__Config
from mgraph_ai.models.Model__MGraph__Attribute                import Model__MGraph__Edge
from mgraph_ai.models.Model__MGraph__Graph                    import Model__MGraph__Graph
from mgraph_ai.models.Model__MGraph__Node                     import Model__MGraph__Node
from osbot_utils.helpers                                      import Random_Guid

class Model__Mermaid__Graph(Model__MGraph__Graph):
    edges  : Dict[Random_Guid, Model__MGraph__Edge]
    nodes  : Dict[Random_Guid, Model__MGraph__Node]
    config : Schema__Mermaid__Graph__Config

    def add_node(self, **kwargs):
        new_node = Model__Mermaid__Node(**kwargs)
        self.nodes[new_node.node_id] = new_node
        return new_node

    def nodes(self):
        for node in self.model.nodes.values():
            yield Model__Mermaid__Node(data = node)

    def edges(self):
        for node in self.model.edges.values():
            yield Model__Mermaid__Node(data = node)