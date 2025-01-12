from unittest                                                   import TestCase
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute         import Schema__MGraph__Attribute
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge              import Schema__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config      import Schema__MGraph__Edge__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph__Config     import Schema__MGraph__Graph__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node              import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data        import Schema__MGraph__Node__Data
from osbot_utils.utils.Objects                                  import __
from mgraph_ai.mgraph.schemas.Schema__MGraph__Default__Types    import Schema__MGraph__Default__Types

class test_Schema__MGraph__Default__Types(TestCase):

    def test__init__(self):
        with Schema__MGraph__Default__Types() as _:
            assert _.obj() == __(attribute_type    = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute.Schema__MGraph__Attribute'         ,
                                 edge_type         = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Edge.Schema__MGraph__Edge'                   ,
                                 edge_config_type  = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config.Schema__MGraph__Edge__Config'   ,
                                 graph_config_type = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Graph__Config.Schema__MGraph__Graph__Config' ,
                                 node_type         = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Node.Schema__MGraph__Node'                   ,
                                 node_data_type    = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data.Schema__MGraph__Node__Data'       )

            assert _.attribute_type     is Schema__MGraph__Attribute
            assert _.edge_type          is Schema__MGraph__Edge
            assert _.edge_config_type   is Schema__MGraph__Edge__Config
            assert _.graph_config_type  is Schema__MGraph__Graph__Config
            assert _.node_type          is Schema__MGraph__Node
            assert _.node_data_type    is Schema__MGraph__Node__Data