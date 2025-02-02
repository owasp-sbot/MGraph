from typing                                                    import Type
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge__Config     import Schema__MGraph__Edge__Config
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node import Schema__Mermaid__Node

class Schema__Mermaid__Edge__Config(Schema__MGraph__Edge__Config):
    edge_mode        : str
    output_node_from : bool = False
    output_node_to   : bool = False
