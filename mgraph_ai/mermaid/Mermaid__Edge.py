from osbot_utils.utils.Str                           import safe_str
from mgraph_ai.core.MGraph__Edge                     import MGraph__Edge
from mgraph_ai.mermaid.Mermaid__Node import Mermaid__Node, LINE_PADDING
from mgraph_ai.mermaid.configs.Mermaid__Edge__Config import Mermaid__Edge__Config


class Mermaid__Edge(MGraph__Edge):
    config    : Mermaid__Edge__Config
    from_node : Mermaid__Node
    to_node   : Mermaid__Node

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

    def render_edge(self):
        from_node_key = safe_str(self.from_node.key)
        to_node_key   = safe_str(self.to_node  .key)
        if self.config.output_node_from:
            from_node_key =  self.from_node.render_node(include_padding=False) #f'{edge.from_node.key}["{edge.from_node.label}"]'
        if self.config.output_node_to:
            to_node_key   = self.to_node.render_node(include_padding=False   ) #f'{edge.to_node  .key}["{edge.to_node  .label}"]'
        if self.config.edge_mode == 'lr_using_pipe':
            link_code      = f'-->|{self.label}|'
        elif self.label:
            link_code      = f'--"{self.label}"-->'
        else:
            link_code      = '-->'
        edge_code      = f'{LINE_PADDING}{from_node_key} {link_code} {to_node_key}'
        return edge_code