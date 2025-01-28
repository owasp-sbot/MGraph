from unittest                                                     import TestCase
from mgraph_ai.query.actions.MGraph__Query__Export__View          import MGraph__Query__Export__View
from mgraph_ai.providers.json.MGraph__Json                        import MGraph__Json
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Graph  import Domain__MGraph__Json__Graph
from osbot_utils.utils.Json                                       import json__equals__list_and_set


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
        cls.mgraph_json.load().from_data(cls.test_data)
        cls.query = cls.mgraph_json.query().setup()


    def test__export_view__no_filter(self):
        with self.query as _:
            export_view           = MGraph__Query__Export__View(mgraph_query=_)
            view_graph            = export_view.export()
            mgraph_json__exported = MGraph__Json(graph=view_graph)
            dict__original_graph  = self.mgraph_json.export().to_dict()
            dict__exported_graph  = mgraph_json__exported.export().to_dict()

            assert type(mgraph_json__exported) is MGraph__Json
            assert type(view_graph           ) is Domain__MGraph__Json__Graph

            assert json__equals__list_and_set(dict__original_graph, dict__exported_graph)


            # self.mgraph_json.screenshot().save().dot__schema()
            # json_graph__exported.screenshot().save().dot__schema()

            # _.name('nested')
            # assert len(edges_ids) == 2
            # assert len(nodes_ids) == 1
            # view_graph = export_view.export()
            # assert type(view_graph) is Domain__MGraph__Json__Graph
            #mgraph_2 = MGraph__Json(graph=view_graph)
            # load_dotenv()
            # pprint(mgraph_2.json())
            #pprint(mgraph_2.screenshot().dot())            # this need a root node (which should be the view_id)

            #_.print_stats()






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

