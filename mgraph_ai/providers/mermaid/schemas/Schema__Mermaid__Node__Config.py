from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Config            import Schema__MGraph__Node__Config
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Shape import Schema__Mermaid__Node__Shape

class Schema__Mermaid__Node__Config(Schema__MGraph__Node__Config):
    markdown         : bool
    node_shape       : Schema__Mermaid__Node__Shape = Schema__Mermaid__Node__Shape.default
    show_label       : bool = True
    wrap_with_quotes : bool = True               # todo: add support for only using quotes when needed
    value_type       : type                      # todo: remove when TypeSafe BUG is fixed
