from typing                                              import List

from mgraph_ai.mermaid.Mermaid__Node import LINE_PADDING
from osbot_utils.utils.Str import safe_str

from mgraph_ai.mermaid.Mermaid__Graph import Mermaid__Graph
from osbot_utils.type_safe.Type_Safe                  import Type_Safe
from mgraph_ai.mermaid.configs.Mermaid__Render__Config   import Mermaid__Render__Config
from mgraph_ai.mermaid.models.Mermaid__Diagram_Direction import Diagram__Direction
from mgraph_ai.mermaid.models.Mermaid__Diagram__Type     import Diagram__Type


class Mermaid__Renderer(Type_Safe):
    config            : Mermaid__Render__Config
    diagram_direction : Diagram__Direction = Diagram__Direction.LR
    diagram_type      : Diagram__Type      = Diagram__Type.graph
    graph             : Mermaid__Graph
    mermaid_code      : List


    def add_line(self, line):
        self.mermaid_code.append(line)
        return line

    def code(self, nodes, edges):
        self.code_create(nodes, edges)
        return '\n'.join(self.mermaid_code)

    def code_create(self, nodes, edges, recreate=False):
        with self as _:
            if recreate:                            # if recreate is True, reset the code
                _.reset_code()
            elif self.mermaid_code:                 # if the code has already been created, don't create it
                return self                         #   todo: find a better way to do this, namely around the concept of auto detecting (on change) when the recreation needs to be done (vs being able to use the previously calculated data)
            for directive in _.config.directives:
                _.add_line(f'%%{{{directive}}}%%')
            _.add_line(self.graph_header())
            if self.config.add_nodes:
                for node in nodes.values():
                    node_code = self.render_node(node)
                    _.add_line(node_code)
            if self.config.line_before_edges:
                _.add_line('')
            for edge in edges:
                edge_code = self.render_edge(edge)
                _.add_line(edge_code)
        return self



    def graph_header(self):
        # if type(self.diagram_type.value) is str:
        #     value = self.diagram_type.value
        # else:
        #     value = self.diagram_type.name
        value = self.diagram_type.name
        return f'{value} {self.diagram_direction.name}'

    def render_edge(self,edge):
        from_node     = self.graph.node(edge.from_node_id)
        to_node       = self.graph.node(edge.to_node_id)
        from_node_key = safe_str(from_node.key)
        to_node_key   = safe_str(to_node  .key)
        if edge.config.output_node_from:
            from_node_key =  self.render_node(from_node, include_padding=False)
        if edge.config.output_node_to:
            to_node_key   = self.render_node(to_node, include_padding=False   )
        if edge.config.edge_mode == 'lr_using_pipe':
            link_code      = f'-->|{edge.label}|'
        elif edge.label:
            link_code      = f'--"{edge.label}"-->'
        else:
            link_code      = '-->'
        edge_code      = f'{LINE_PADDING}{from_node_key} {link_code} {to_node_key}'
        return edge_code

    def render_node(self, node, include_padding=True):
        left_char, right_char = node.config.node_shape.value

        if node.config.markdown:
            label = f'`{node.label}`'
        else:
            label = node.label

        if node.config.show_label is False:
            node_code = f'{node.key}'
        else:
            if node.config.wrap_with_quotes is False:
                node_code = f'{node.key}{left_char}{label}{right_char}'
            else:
                node_code = f'{node.key}{left_char}"{label}"{right_char}'

        if include_padding:
            node_code = f'{LINE_PADDING}{node_code}'
        return node_code

    def reset_code(self):
        self.mermaid_code = []
        return self