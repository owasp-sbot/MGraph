from mgraph_ai.mgraph.domain.MGraph__Edge                      import MGraph__Edge
from mgraph_ai.providers.mermaid.models.Model__Mermaid__Edge   import Model__Mermaid__Edge
from mgraph_ai.providers.mermaid.models.Model__Mermaid__Graph  import Model__Mermaid__Graph


class Mermaid__Edge(MGraph__Edge):
    edge  : Model__Mermaid__Edge
    graph : Model__Mermaid__Graph
    label : str

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