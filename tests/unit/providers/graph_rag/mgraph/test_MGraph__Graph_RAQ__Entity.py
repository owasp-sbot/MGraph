from unittest                                                               import TestCase

from mgraph_db.providers.graph_rag.mgraph import MGraph__Graph_RAQ__Entity
from mgraph_db.providers.graph_rag.mgraph.schemas.Schema__Graph_RAG__Edges import Schema__Graph_RAG__Edge__Confidence
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Entity__Data import Schema__Graph_RAG__Entity__Data

from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Entity        import Schema__Graph_RAG__Entity
from mgraph_db.providers.graph_rag.actions.Graph_RAG__Document__Processor   import Graph_RAG__Document__Processor

from osbot_utils.utils.Dev                                                  import pprint
from osbot_utils.utils.Env import load_dotenv, not_in_github_action
from osbot_utils.utils.Http import current_host_online


class test_MGraph__Graph_RAQ__Entity(TestCase):

    @classmethod
    def setUpClass(cls):
        #load_dotenv()
        cls.sample_text  = "cyber-news-1"                                        # Using cached test data
        cls.processor    = Graph_RAG__Document__Processor()
        cls.llm_entities = cls.processor.extract_entities(cls.sample_text)       # create test entities
        cls.entities     = cls.llm_entities.entities
        cls.create_png   = False

    def setUp(self):
        self.mgraph_entity = MGraph__Graph_RAQ__Entity()

    def tearDown(self):
        # with self.mgraph_entity as _:
        #     pprint(_.export().to__json())
        if self.create_png:
            with self.mgraph_entity.screenshot() as _:
                    load_dotenv()
                    _.save_to(f'{self.__class__.__name__}.png')
                    _.show_node_value()
                    _.show_edge_type()
                    #_.show_node_id()
                    _.dot()
                # if current_host_online():
                # else:
                #     print('Currenly offline, so not creating png')


    def test_setUpClass(self):
        assert len(self.entities) == 4
        with self.entities[0] as entity_data:
            assert type(entity_data) is Schema__Graph_RAG__Entity__Data



    def test_create_graph(self):
        entity : Schema__Graph_RAG__Entity__Data = self.entities[0]
        assert type(entity) is Schema__Graph_RAG__Entity__Data

        with self.mgraph_entity.edit() as _:
            ## pprint(entity.json())
            root_node         = _.new_value(f'entity_id: {entity.entity_id}')
            value__confidence = _.new_value(entity.confidence)
            _.connect_nodes(root_node, value__confidence, Schema__Graph_RAG__Edge__Confidence)

        assert _.data().stats() == {'edges_ids': 1, 'nodes_ids': 2}

