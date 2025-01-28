from unittest                                                     import TestCase
from mgraph_ai.providers.json.actions.MGraph__Json__Screenshot    import ENV_NAME__URL__MGRAPH_AI_SERVERLESS
from osbot_utils.utils.Env                                        import set_env
from mgraph_ai.query.actions.MGraph__Query__Export__View          import MGraph__Query__Export__View
from mgraph_ai.providers.json.MGraph__Json                        import MGraph__Json
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Graph  import Domain__MGraph__Json__Graph
from mgraph_ai.providers.json.models.Model__MGraph__Json__Graph   import Model__MGraph__Json__Graph
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Graph import Schema__MGraph__Json__Graph
from mgraph_ai.query.models.Model__MGraph__Query__View            import Model__MGraph__Query__View


class test_MGraph__Query__Export__View(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mgraph_json = MGraph__Json()
        cls.test_data = {   'name'  : 'root'                      ,
                            'values': [1, 2, 3]                   ,
                            'nested': { 'name' : 'child'          ,
                                        'value': 42 }             ,
                            'items' : [{ 'id': 1, 'name': 'first' },
                                       { 'id': 2, 'name': 'second'}]}
        #cls.test_data = {}
        cls.mgraph_json.load().from_data(cls.test_data)

        cls.query = cls.mgraph_json.query().setup()

    # todo: finish this test the the 'views nodes' are working
    def test__export_view(self):
        with self.query as _:
            #result = self.query.export_view()
            _.name('nested')
            graph_domain = _.mgraph_data.graph
            graph_model  = graph_domain.model
            graph_schema = graph_model.data
            target_view   = _.current_view()
            nodes_ids     = target_view.nodes_ids()
            edges_ids     = target_view.edges_ids()
            assert type(graph_domain) is Domain__MGraph__Json__Graph
            assert type(graph_model ) is Model__MGraph__Json__Graph
            assert type(graph_schema) is Schema__MGraph__Json__Graph
            assert type(target_view)  is Model__MGraph__Query__View
            assert type(edges_ids)    is set
            assert type(nodes_ids)    is set

            assert len(edges_ids) == 2
            assert len(nodes_ids) == 1
            kwargs = dict(graph_domain = graph_domain,
                          graph_model  = graph_model ,
                          graph_schema = graph_schema,
                          edges_ids    = edges_ids   ,
                          nodes_ids    = nodes_ids   )
            export_view = MGraph__Query__Export__View(**kwargs)

            view_graph = export_view.export()
            assert type(view_graph) is Domain__MGraph__Json__Graph
            #mgraph_2 = MGraph__Json(graph=view_graph)
            # load_dotenv()
            # pprint(mgraph_2.json())
            #pprint(mgraph_2.screenshot().dot())            # this need a root node (which should be the view_id)

            #_.print_stats()

    def test__create_dot__no_filter(self):
        set_env(ENV_NAME__URL__MGRAPH_AI_SERVERLESS, 'http://localhost:8080')
        with self.mgraph_json.data() as _:
            root_property_id = _.root_property_id()

        with self.mgraph_json.edit() as _:
            property_1 = _.add_property('abc' , node_id=root_property_id)
            property_2 = _.add_property('1234', node_id=root_property_id, value='xyz')
            _.add_value   ('12345', node_id=property_1.node_id)

        assert self.mgraph_json.export().to_dict() == {'1234': 'xyz', 'abc': '12345' ,
                                                       ** self.test_data}

            #edge_1 = _.new_edge(from_node_id=root_property_id, to_node_id=property_node.node_id)

        #     pprint(property_node.node.json())
        #     root_id = _.graph.root().node_id
        #     print(root_id)

        #     # node_1 = _.new_node(name='abc')
        #     # node_2 = _.new_node(value='xyz')
        #     # pprint(_.graph.model.data.graph_data.root_id)
        #     #
        #     # edge_1 = _.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
        #     # #edge_2 = _.new_edge(from_node_id=root_id, to_node_id=node_1.node_id)

        # with self.mgraph_json.query() as _:
        #     _.print_stats()

        # with self.mgraph_json as _:
        #     _.screenshot().save_to('./dot-graph.png').dot()
        #     #_.screenshot().save_to('./dot-graph.png').dot__just_ids()
        #
        #     pprint(_.export().to_dict())
        #     #_.query().re_index()

