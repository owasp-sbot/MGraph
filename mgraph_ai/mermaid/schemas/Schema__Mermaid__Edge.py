from mgraph_ai.mermaid.schemas.Schema__Mermaid__Node import Schema__Mermaid__Node
from osbot_utils.helpers.Safe_Id                     import Safe_Id
from mgraph_ai.schemas.Schema__MGraph__Edge          import Schema__MGraph__Edge

class Schema__Mermaid__Edge(Schema__MGraph__Edge):
    label         : Safe_Id

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.from_node_type = Schema__Mermaid__Node
        self.to_node_type   = Schema__Mermaid__Node
