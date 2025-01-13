from unittest import TestCase

from osbot_utils.utils.Objects import obj, __

from osbot_utils.utils.Dev import pprint

from mgraph_ai.mgraph.MGraph import MGraph
from mgraph_ai.mgraph.actions.MGraph__Export import MGraph__Export


class test_MGraph__Export(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.mgraph        = MGraph()
        cls.mgraph_export = cls.mgraph.export()

    def test_to__mgraph_json(self):
        data = self.mgraph_export.to__mgraph_json()

        assert data == self.mgraph.graph.model.data.json()

        assert obj(data) == __(edges        =__()                                                                   ,
                               graph_data   =__()                                                                   ,
                               graph_id     = self.mgraph.data().graph_id()                                         ,
                               graph_type   ='mgraph_ai.mgraph.schemas.Schema__MGraph__Graph.Schema__MGraph__Graph' ,
                               nodes        = __()                                                                  ,
                               schema_types = __(edge_type        = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Edge.Schema__MGraph__Edge',
                                                 edge_config_type = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config.Schema__MGraph__Edge__Config',
                                                 graph_data_type  = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Graph__Data.Schema__MGraph__Graph__Data',
                                                 node_type        = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Node.Schema__MGraph__Node',
                                                 node_data_type   = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data.Schema__MGraph__Node__Data'))


        #expected_data = {
                        #     "nodes": {
                        #         "123e4567": {},
                        #         "234e5678": {},
                        #         "345e6789": {}
                        #     },
                        #     "edges": {
                        #         "456e7890": {
                        #             "from_node_id": "123e4567",
                        #             "to_node_id": "234e5678"
                        #         },
                        #         "567e8901": {
                        #             "from_node_id": "123e4567",
                        #             "to_node_id": "345e6789"
                        #         }
                        #     }
                        # }
