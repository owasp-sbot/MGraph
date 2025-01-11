from mgraph_ai.mgraph.domain.MGraph__Edge                              import MGraph__Edge
from mgraph_ai.providers.mermaid.models.Model__Mermaid__Edge           import Model__Mermaid__Edge
from mgraph_ai.providers.mermaid.models.Model__Mermaid__Graph          import Model__Mermaid__Graph
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge__Config import Schema__Mermaid__Edge__Config
from osbot_utils.type_safe.methods.type_safe_property                  import set_as_property


class Mermaid__Edge(MGraph__Edge):
    edge  : Model__Mermaid__Edge
    graph : Model__Mermaid__Graph
    label = set_as_property('edge.data', 'label')


    def config(self) -> Schema__Mermaid__Edge__Config:
        return super().config()

    def edge_mode(self, edge_mode):
        self.config().edge_mode = edge_mode
        return self

    def edge_mode__lr_using_pipe(self):
        return self.edge_mode('lr_using_pipe')

    def from_node_id(self):
        return self.edge.from_node_id()

    def output_node_from(self, value=True):
        self.config().output_node_from = value
        return self

    def output_node_to(self, value=True):
        self.config().output_node_to = value
        return self

    def to_node_id(self):
        return self.edge.to_node_id()