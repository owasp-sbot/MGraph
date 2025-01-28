import pytest

from unittest                                                     import TestCase
from osbot_utils.utils.Env                                        import load_dotenv
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge                import Schema__MGraph__Edge
from osbot_utils.type_safe.shared.Type_Safe__Cache                import type_safe_cache
from osbot_utils.utils.Objects                                    import type_full_name
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Edge  import Schema__MGraph__Json__Edge
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
        cls.test_data = {  'name'  : 'root'                      ,
                            'values': [1, 2, 3]                   ,
                            'nested': { 'name' : 'child'          ,
                                        'value': 42 }             ,
                            'items' : [{ 'id': 1, 'name': 'first' },
                                       { 'id': 2, 'name': 'second'}]}
        cls.mgraph_json.load().from_data(cls.test_data)

        cls.query = cls.mgraph_json.query().setup()


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
            mgraph_2 = MGraph__Json(graph=view_graph)
            # load_dotenv()
            # pprint(mgraph_2.json())
            # pprint(mgraph_2.screenshot().dot())            # this need a root node (which should be the view_id)

            #_.print_stats()