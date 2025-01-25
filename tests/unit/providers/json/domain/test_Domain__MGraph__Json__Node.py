from unittest                                                   import TestCase
from mgraph_ai.mgraph.domain.Domain__MGraph__Node               import Domain__MGraph__Node
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node import Domain__MGraph__Json__Node
from osbot_utils.utils.Objects                                  import __


class test_Domain__MGraph__Json__Node(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.domain_node = Domain__MGraph__Json__Node()

    def test__init__(self):
        with self.domain_node as _:
            assert isinstance(_, Domain__MGraph__Node)
            assert _.obj() == __(node  = __(data        = __(node_data    = __(),
                                                            node_id       = _.node_id,
                                                            node_type     = 'mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node.Schema__MGraph__Json__Node')),
                                 graph = __(data        = __(edges        = __(),
                                                             graph_data   = __(),
                                                             graph_id     = _.graph.graph_id,
                                                             graph_type   = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Graph.Schema__MGraph__Graph',
                                                             nodes        = __(),
                                                             schema_types = __(edge_type        = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Edge.Schema__MGraph__Edge'                  ,
                                                                               edge_config_type = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config.Schema__MGraph__Edge__Config'  ,
                                                                               graph_data_type  = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Graph__Data.Schema__MGraph__Graph__Data'    ,
                                                                               node_type        = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Node.Schema__MGraph__Node'                  ,
                                                                               node_data_type   = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data.Schema__MGraph__Node__Data'     )),
                                            model_types = __(node_model_type = 'mgraph_ai.mgraph.models.Model__MGraph__Node.Model__MGraph__Node',
                                                             edge_model_type = 'mgraph_ai.mgraph.models.Model__MGraph__Edge.Model__MGraph__Edge')))
