from mgraph_ai.core.MGraph__Edge                     import MGraph__Edge
from mgraph_ai.mermaid.Mermaid__Node                 import Mermaid__Node
from mgraph_ai.mermaid.configs.Mermaid__Edge__Config import Mermaid__Edge__Config
from mgraph_ai.mermaid.models.Model__Mermaid__Edge   import Model__Mermaid__Edge


class Mermaid__Edge(MGraph__Edge):
    model          : Model__Mermaid__Edge    
    config         : Mermaid__Edge__Config
    label          : str

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.from_node_type = Mermaid__Node
        self.to_node_type   = Mermaid__Node

    def edge_mode(self, edge_mode):
        self.config.edge_mode = edge_mode
        return self

    def edge_mode__lr_using_pipe(self):
        return self.edge_mode('lr_using_pipe')

    def output_node_from(self, value=True):
        self.config.output_node_from = value
        return self

    def output_node_to(self, value=True):
        self.config.output_node_to = value
        return self