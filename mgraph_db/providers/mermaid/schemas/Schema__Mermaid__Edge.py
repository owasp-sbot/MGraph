from typing                                                            import Type
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Edge__Config import Schema__Mermaid__Edge__Config
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                     import Schema__MGraph__Edge

class Schema__Mermaid__Edge(Schema__MGraph__Edge):
    label         : str
    edge_config   : Schema__Mermaid__Edge__Config
    edge_type     : Type['Schema__Mermaid__Edge']