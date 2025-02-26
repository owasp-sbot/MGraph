from unittest                                                               import TestCase
from mgraph_db.providers.graph_rag.mgraph                                   import MGraph__Graph_RAQ__Entity
from mgraph_db.providers.graph_rag.mgraph.schemas.Schema__Graph_RAG__Edges import Schema__Graph_RAG__Edge__Confidence, \
    Schema__Graph_RAG__Edge__Direct_Relationship, Schema__Graph_RAG__Edge__Relationship_Type, \
    Schema__Graph_RAG__Edge__Strength, Schema__Graph_RAG__Edge__Domain_Relationship, Schema__Graph_RAG__Edge__Concept, \
    Schema__Graph_RAG__Edge__Category, Schema__Graph_RAG__Edge__Entity
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Entity        import Schema__Graph_RAG__Entity
from mgraph_db.providers.graph_rag.actions.Graph_RAG__Document__Processor   import Graph_RAG__Document__Processor
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Env                                                  import load_dotenv


class test_MGraph__Graph_RAQ__Entity(TestCase):

    @classmethod
    def setUpClass(cls):
        #load_dotenv()
        #cls.sample_text = "new GDPR fine in Lisbon on SaaS fintech startup"
        cls.sample_text  = "cyber-news-1"                                        # Using cached test data
        cls.processor    = Graph_RAG__Document__Processor()
        cls.llm_entities = cls.processor.extract_entities(cls.sample_text)       # create test entities
        cls.entities     = cls.llm_entities.entities
        cls.create_png   = True

    def setUp(self):
        self.mgraph_entity = MGraph__Graph_RAQ__Entity()

    def tearDown(self):
        # with self.mgraph_entity as _:
        #     pprint(_.export().to__json())
        if self.create_png:
            with self.mgraph_entity.screenshot() as _:
                with _.export().export_dot() as dot:
                    dot.set_graph__rank_dir__lr()
                    dot.set_node__shape__type__box()
                    dot.set_node__shape__rounded()

                load_dotenv()
                _.save_to(f'{self.__class__.__name__}.png')
                _.show_node_value()
                _.show_edge_type()

                #_.show_node_type()
                _.dot()
                # if current_host_online():
                # else:
                #     print('Currenly offline, so not creating png')


    def test_setUpClass(self):
        assert len(self.entities) == 4
        with self.entities[0] as entity_data:
            assert type(entity_data) is Schema__Graph_RAG__Entity



    def test_create_graph(self):
        for entity in self.entities:
        #entity : Schema__Graph_RAG__Entity =
            assert type(entity) is Schema__Graph_RAG__Entity

            with self.mgraph_entity.edit() as _:
                ## pprint(entity.json())
                root_node                  = _.new_value(entity.name)
                #node__confidence           = _.new_value(entity.confidence)
                #_.connect_nodes(root_node, node__confidence          , Schema__Graph_RAG__Edge__Confidence          )

                for direct_relationship in entity.direct_relationships:
                    node__entity = _.new_value(direct_relationship.entity)
                    _.connect_nodes(root_node, node__entity, Schema__Graph_RAG__Edge__Entity)
                    node__relationship_type   = _.new_value(direct_relationship.relationship_type)
                    _.connect_nodes(node__entity, node__relationship_type, Schema__Graph_RAG__Edge__Relationship_Type)
                    #pprint(_.graph.model.data.json())
                    return
                    node__strength = _.new_value(direct_relationship.strength)
                    _.connect_nodes(node__entity, node__strength          , Schema__Graph_RAG__Edge__Strength         )
                    #{'entity': 'Continuous Integration',
                    # 'relationship_type': 'is a type of',
                    # 'strength': 0.8}
                    #pprint(direct_relationship.json())
            #assert _.data().stats() == {'edges_ids': 1, 'nodes_ids': 2}
            for domain_relationship in entity.domain_relationships:
                pprint(domain_relationship.json())
                node__concept = _.new_value(domain_relationship.concept)
                node__category = _.new_value(domain_relationship.category)
                _.connect_nodes(root_node, node__concept, Schema__Graph_RAG__Edge__Concept)
                _.connect_nodes(node__concept, node__category, Schema__Graph_RAG__Edge__Category)
            break
