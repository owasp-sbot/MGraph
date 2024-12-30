from mgraph_ai.mermaid.configs.Mermaid__Node__Config   import Mermaid__Node__Config
from mgraph_ai.mermaid.models.Mermaid__Node__Shape     import Mermaid__Node__Shape
from mgraph_ai.core.MGraph__Node                       import MGraph__Node

LINE_PADDING = '    '

class Mermaid__Node(MGraph__Node):
    config : Mermaid__Node__Config

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.label:
            self.label = self.key

    def render_node(self, include_padding=True):
        left_char, right_char = self.config.node_shape.value

        if self.config.markdown:
            label = f'`{self.label}`'
        else:
            label = self.label


        if self.config.show_label is False:
            node_code = f'{self.key}'
        else:
            if self.config.wrap_with_quotes is False:
                node_code = f'{self.key}{left_char}{label}{right_char}'
            else:
                node_code = f'{self.key}{left_char}"{label}"{right_char}'

        if include_padding:
            node_code = f'{LINE_PADDING}{node_code}'
        return node_code

    def markdown(self, value=True):
        self.config.markdown = value
        return self

    def shape(self, shape=None):
        self.config.node_shape = Mermaid__Node__Shape.get_shape(shape)
        return self


    def shape_asymmetric        (self): self.config.node_shape = Mermaid__Node__Shape.asymmetric        ; return self
    def shape_circle            (self): self.config.node_shape = Mermaid__Node__Shape.circle            ; return self
    def shape_cylindrical       (self): self.config.node_shape = Mermaid__Node__Shape.cylindrical       ; return self
    def shape_default           (self): self.config.node_shape = Mermaid__Node__Shape.default           ; return self
    def shape_double_circle     (self): self.config.node_shape = Mermaid__Node__Shape.double_circle     ; return self
    def shape_hexagon           (self): self.config.node_shape = Mermaid__Node__Shape.hexagon           ; return self
    def shape_parallelogram     (self): self.config.node_shape = Mermaid__Node__Shape.parallelogram     ; return self
    def shape_parallelogram_alt (self): self.config.node_shape = Mermaid__Node__Shape.parallelogram_alt ; return self
    def shape_stadium           (self): self.config.node_shape = Mermaid__Node__Shape.stadium           ; return self
    def shape_subroutine        (self): self.config.node_shape = Mermaid__Node__Shape.subroutine        ; return self
    def shape_rectangle         (self): self.config.node_shape = Mermaid__Node__Shape.rectangle         ; return self
    def shape_rhombus           (self): self.config.node_shape = Mermaid__Node__Shape.rhombus           ; return self
    def shape_round_edges       (self): self.config.node_shape = Mermaid__Node__Shape.round_edges       ; return self
    def shape_trapezoid         (self): self.config.node_shape = Mermaid__Node__Shape.trapezoid         ; return self
    def shape_trapezoid_alt     (self): self.config.node_shape = Mermaid__Node__Shape.trapezoid_alt     ; return self



    def wrap_with_quotes(self, value=True):
        self.config.wrap_with_quotes = value
        return self

    def show_label(self, value=True):
        self.config.show_label = value
        return self