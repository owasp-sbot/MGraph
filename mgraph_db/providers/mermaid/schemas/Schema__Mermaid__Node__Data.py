from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data              import Schema__MGraph__Node__Data
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node__Shape import Schema__Mermaid__Node__Shape

class Schema__Mermaid__Node__Data(Schema__MGraph__Node__Data):
    markdown         : bool
    node_shape       : Schema__Mermaid__Node__Shape = Schema__Mermaid__Node__Shape.default
    show_label       : bool = True
    wrap_with_quotes : bool = True               # todo: add support for only using quotes when needed
