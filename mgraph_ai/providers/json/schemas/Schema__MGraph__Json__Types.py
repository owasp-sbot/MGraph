from typing                                                 import Type

from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Edge import Schema__MGraph__Json__Edge
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node import Schema__MGraph__Json__Node
from osbot_utils.type_safe.Type_Safe                        import Type_Safe
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge          import Schema__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config  import Schema__MGraph__Edge__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph__Data   import Schema__MGraph__Graph__Data
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node          import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data    import Schema__MGraph__Node__Data

class Schema__MGraph__Json__Types(Type_Safe):
    edge_type        : Type[Schema__MGraph__Json__Edge   ]
    edge_config_type : Type[Schema__MGraph__Edge__Config ]
    graph_data_type  : Type[Schema__MGraph__Graph__Data]
    node_type        : Type[Schema__MGraph__Json__Node   ]
    node_data_type   : Type[Schema__MGraph__Node__Data   ]
