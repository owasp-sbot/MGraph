from unittest                                                               import TestCase

from mgraph_db.providers.graph_rag.mgraph import MGraph__Graph_RAQ__Entity
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Entity__Data import Schema__Graph_RAG__Entity__Data

from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Entity        import Schema__Graph_RAG__Entity
from mgraph_db.providers.graph_rag.actions.Graph_RAG__Document__Processor   import Graph_RAG__Document__Processor

from osbot_utils.utils.Dev                                                  import pprint
from osbot_utils.utils.Env import load_dotenv
from osbot_utils.utils.Http import current_host_online


class test_MGraph__Graph_RAQ__Entity(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sample_text = "cyber-news-1"                                        # Using cached test data
        cls.processor   = Graph_RAG__Document__Processor()
        cls.entities    = cls.processor.extract_entities(cls.sample_text)       # create test entities

    def setUp(self):
        self.mgraph_entity = MGraph__Graph_RAQ__Entity()

    def tearDown(self):
        with self.mgraph_entity as _:
            pprint(_.export().to__json())

        # with self.mgraph_entity.screenshot() as _:
        #     if current_host_online():
        #         load_dotenv()
        #         png_file_name = f'{self.__class__.__name__}.png'
        #         _.save_to(png_file_name)
        #         _.dot()
        #     else:
        #         print('Currenly offline, so not creating png')


    def test_setUpClass(self):
        assert len(self.entities) == 4
        with self.entities[0] as _:
            entity_data = _.node_data
            assert type(entity_data) is Schema__Graph_RAG__Entity__Data
            pprint(entity_data.json())

    def test_create_graph(self):
        entity = self.entities[0].node_data
        pprint(entity.json())
        with self.mgraph_entity.edit() as _:

            root_node         = _.new_value(entity.entity_id)
            value__confidence = _.new_value(entity.confidence)
            _.connect_nodes(root_node, value__confidence)

