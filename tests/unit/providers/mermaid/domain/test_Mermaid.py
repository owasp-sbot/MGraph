from unittest                                                   import TestCase
from mgraph_ai.providers.mermaid.domain.Domain__Mermaid__Graph  import Domain__Mermaid__Graph
from osbot_utils.helpers.Obj_Id                                 import is_obj_id
from osbot_utils.utils.Objects                                  import __, full_type_name
from mgraph_ai.providers.mermaid.MGraph__Mermaid                import MGraph__Mermaid


class test_Mermaid(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mermaid = MGraph__Mermaid()

    def test__init__(self):
        with self.mermaid as _:
            graph_id = _.data().graph_id()
            assert type(_) is MGraph__Mermaid
            assert is_obj_id(graph_id) is True
            assert _.obj()             == __(graph=__(domain_types   = __(node_domain_type='mgraph_ai.providers.mermaid.domain.Domain__Mermaid__Node.Domain__Mermaid__Node',
                                                                         edge_domain_type='mgraph_ai.providers.mermaid.domain.Domain__Mermaid__Edge.Domain__Mermaid__Edge'),
                                                      graph_type    = full_type_name(Domain__Mermaid__Graph)                                                               ,
                                                      model         = __(data=__(schema_types  = __(edge_type         = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge.Schema__Mermaid__Edge'                  ,
                                                                                                    edge_config_type  = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge__Config.Schema__Mermaid__Edge__Config'  ,
                                                                                                    graph_data_type   = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Graph__Config.Schema__Mermaid__Graph__Config',
                                                                                                    node_type         = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node.Schema__Mermaid__Node'                  ,
                                                                                                    node_data_type  = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Data.Schema__Mermaid__Node__Data'  ),
                                                                                 edges        = __(),
                                                                                 graph_data   = __(allow_circle_edges    = False,
                                                                                                   allow_duplicate_edges = False,
                                                                                                   graph_title           = ''   ),
                                                                                 graph_id     = graph_id                         ,
                                                                                 graph_type   = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Graph.Schema__Mermaid__Graph',
                                                                                 mermaid_code = [],
                                                                                 nodes        = __(),
                                                                                 render_config=__(add_nodes         = True   ,
                                                                                                  diagram_direction = 'LR'   ,
                                                                                                  diagram_type      = 'graph',
                                                                                                  line_before_edges = True   ,
                                                                                                  directives        = []     )),
                                                                         model_types =__(node_model_type='mgraph_ai.providers.mermaid.models.Model__Mermaid__Node.Model__Mermaid__Node',
                                                                                          edge_model_type='mgraph_ai.providers.mermaid.models.Model__Mermaid__Edge.Model__Mermaid__Edge'))))
