from mgraph_db.providers.mermaid.models.Model__Mermaid__Types   import Model__Mermaid__Types
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Graph import Schema__Mermaid__Graph
from mgraph_db.mgraph.models.Model__MGraph__Graph               import Model__MGraph__Graph

class Model__Mermaid__Graph(Model__MGraph__Graph):
    data          : Schema__Mermaid__Graph
    model_types : Model__Mermaid__Types



    # def add_node(self, **kwargs):
    #     new_node = Model__Mermaid__Node(**kwargs)
    #     self.nodes[new_node.node_id] = new_node
    #     return new_node
    #
    # def nodes(self):
    #     for node in self.model.nodes.values():
    #         yield Model__Mermaid__Node(data = node)
    #
    # def edges(self):
    #     for node in self.model.edges.values():
    #         yield Model__Mermaid__Node(data = node)