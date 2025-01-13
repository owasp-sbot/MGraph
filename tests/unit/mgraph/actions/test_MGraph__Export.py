from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from mgraph_ai.mgraph.MGraph import MGraph
from mgraph_ai.mgraph.actions.MGraph__Export import MGraph__Export


class test_MGraph__Export(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.mgraph        = MGraph()
        cls.mgraph_export = cls.mgraph.export()

    def test_to_json(self):
        data = self.mgraph_export.to_json()

        pprint(data)


        expected_data = {
                            "nodes": {
                                "123e4567": {},
                                "234e5678": {},
                                "345e6789": {}
                            },
                            "edges": {
                                "456e7890": {
                                    "from_node_id": "123e4567",
                                    "to_node_id": "234e5678"
                                },
                                "567e8901": {
                                    "from_node_id": "123e4567",
                                    "to_node_id": "345e6789"
                                }
                            }
                        }
