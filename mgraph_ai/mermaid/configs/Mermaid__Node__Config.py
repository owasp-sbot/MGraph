from osbot_utils.base_classes.Type_Safe            import Type_Safe
from mgraph_ai.mermaid.models.Mermaid__Node__Shape import Mermaid__Node__Shape


class Mermaid__Node__Config(Type_Safe):
    markdown         : bool
    node_shape       : Mermaid__Node__Shape = Mermaid__Node__Shape.default
    show_label       : bool = True
    wrap_with_quotes : bool = True               # todo: add support for only using quotes when needed
