from unittest                                                                    import TestCase
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute                          import Schema__MGraph__Attribute
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge                               import Schema__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config                       import Schema__MGraph__Edge__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data                         import Schema__MGraph__Node__Data
from mgraph_ai.providers.file_system.schemas.Schema__File_System__Default__Types import Schema__File_System__Default__Types
from mgraph_ai.providers.file_system.schemas.Schema__File_System__Graph__Config  import Schema__File_System__Graph__Config
from mgraph_ai.providers.file_system.schemas.Schema__Folder__Node                import Schema__Folder__Node
from osbot_utils.utils.Objects                                                   import __

class test_Schema__File_System__Default__Types(TestCase):

    def test__init__(self):
        with Schema__File_System__Default__Types() as _:
            assert _.obj() == __(graph_config_type = 'mgraph_ai.providers.file_system.schemas.Schema__File_System__Graph__Config.Schema__File_System__Graph__Config' ,
                                 node_type         = 'mgraph_ai.providers.file_system.schemas.Schema__Folder__Node.Schema__Folder__Node'                             ,
                                 attribute_type    = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute.Schema__MGraph__Attribute'                                  ,
                                 edge_type         = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Edge.Schema__MGraph__Edge'                                            ,
                                 edge_config_type  = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config.Schema__MGraph__Edge__Config'                            ,
                                 node_data_type    = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data.Schema__MGraph__Node__Data'                                )

            assert _.graph_config_type  is Schema__File_System__Graph__Config
            assert _.node_type          is Schema__Folder__Node
            assert _.attribute_type     is Schema__MGraph__Attribute
            assert _.edge_type          is Schema__MGraph__Edge
            assert _.edge_config_type   is Schema__MGraph__Edge__Config
            assert _.node_data_type is Schema__MGraph__Node__Data