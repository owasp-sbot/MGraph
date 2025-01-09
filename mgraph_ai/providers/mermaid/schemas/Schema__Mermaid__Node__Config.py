from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Shape import Schema__Mermaid__Node__Shape
from osbot_utils.type_safe.Type_Safe                                  import Type_Safe


class Schema__Mermaid__Node__Config(Type_Safe):
    markdown         : bool
    node_shape       : Schema__Mermaid__Node__Shape = Schema__Mermaid__Node__Shape.default
    show_label       : bool = True
    wrap_with_quotes : bool = True               # todo: add support for only using quotes when needed
