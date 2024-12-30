from typing import List

from osbot_utils.base_classes.Kwargs_To_Self                        import Kwargs_To_Self
from mgraph_ai.mermaid.configs.Mermaid__Render__Config     import Mermaid__Render__Config
from mgraph_ai.mermaid.models.Mermaid__Diagram_Direction   import Diagram__Direction
from mgraph_ai.mermaid.models.Mermaid__Diagram__Type       import Diagram__Type


class Mermaid__Renderer(Kwargs_To_Self):
    config            : Mermaid__Render__Config
    mermaid_code      : List
    diagram_direction : Diagram__Direction = Diagram__Direction.LR
    diagram_type      : Diagram__Type      = Diagram__Type.graph


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
                for node in nodes:
                    node_code = node.render_node()
                    _.add_line(node_code)
            if self.config.line_before_edges:
                _.add_line('')
            for edge in edges:
                edge_code = edge.render_edge()
                _.add_line(edge_code)
        return self



    def graph_header(self):
        # if type(self.diagram_type.value) is str:
        #     value = self.diagram_type.value
        # else:
        #     value = self.diagram_type.name
        value = self.diagram_type.name
        return f'{value} {self.diagram_direction.name}'

    def reset_code(self):
        self.mermaid_code = []
        return self