from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node import Schema__Mermaid__Node
from mgraph_db.mgraph.models.Model__MGraph__Node               import Model__MGraph__Node

class Model__Mermaid__Node(Model__MGraph__Node):
    data  : Schema__Mermaid__Node

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ensure_label_is_set()

    def ensure_label_is_set(self):
        with self.data  as _:
            if not _.label:
                _.label = _.key                                  # todo: add scenario when for when key is not set