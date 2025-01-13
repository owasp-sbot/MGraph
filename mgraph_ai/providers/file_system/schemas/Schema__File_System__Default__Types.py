from typing                                                                     import Type
from mgraph_ai.mgraph.schemas.Schema__MGraph__Default__Types                    import Schema__MGraph__Default__Types
from mgraph_ai.providers.file_system.schemas.Schema__File_System__Graph__Config import Schema__File_System__Graph__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data                        import Schema__MGraph__Node__Data
from mgraph_ai.providers.file_system.schemas.Schema__Folder__Node               import Schema__Folder__Node


class Schema__File_System__Default__Types(Schema__MGraph__Default__Types):
    # edge_type        : Type[Schema__MGraph__Edge              ]
    # edge_config_type : Type[Schema__MGraph__Edge__Config      ]
    graph_data_type: Type[Schema__File_System__Graph__Config]
    node_type        : Type[Schema__Folder__Node              ]
    node_data_type   : Type[Schema__MGraph__Node__Data        ]
    #node_config_type : Type[Schema__MGraph__Node__Config      ]
