from mgraph_ai.mermaid.schemas.Schema__Mermaid__Node         import Schema__Mermaid__Node
from mgraph_ai.mermaid.schemas.Schema__Mermaid__Node__Config import Schema__Mermaid__Node__Config
from mgraph_ai.models.Model__MGraph__Node                    import Model__MGraph__Node

class Model__Mermaid__Node(Model__MGraph__Node):
    data  : Schema__Mermaid__Node
    config: Schema__Mermaid__Node__Config

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        from osbot_utils.utils.Dev import pprint
        pprint(kwargs.get('data'  , {}))
        pprint(Schema__Mermaid__Node.from_json({}))
        #self.data   = Schema__Mermaid__Node        .from_json(kwargs.get('data'  , {}))
        #self.config = Schema__Mermaid__Node__Config.from_json(kwargs.get('config', {}))
        self.ensure_label_is_set()

    def ensure_label_is_set(self):
        with self.data  as _:
            if not _.label:
                _.label = _.key                                  # todo: add scenario when for when key is not set