from unittest                                                               import TestCase
from mgraph_ai.providers.mermaid.MGraph__Mermaid                            import MGraph__Mermaid
from mgraph_ai.providers.mermaid.domain.Domain__Mermaid__Edge               import Domain__Mermaid__Edge
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Diagram_Direction import Schema__Mermaid__Diagram__Direction
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Render__Config    import Schema__Mermaid__Render__Config
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Diagram__Type     import Schema__Mermaid__Diagram__Type
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Data        import Schema__Mermaid__Node__Data
from osbot_utils.helpers.Safe_Id                                            import Safe_Id
from osbot_utils.utils.Objects                                              import __, obj
from mgraph_ai.providers.mermaid.domain.Domain__Mermaid__Node               import Domain__Mermaid__Node
from osbot_utils.utils.Misc                                                 import is_guid
from mgraph_ai.mgraph.actions.MGraph__Edit                                  import MGraph__Edit
from mgraph_ai.providers.mermaid.actions.Mermaid__Edit                      import Mermaid__Edit
from mgraph_ai.providers.mermaid.domain.Domain__Mermaid__Graph              import Domain__Mermaid__Graph


class test__Mermaid__Edit(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mermaid         = MGraph__Mermaid()
        cls.mermaid__edit   = cls.mermaid.edit()
        cls.mermaid__render = cls.mermaid.render()

    def test__init__(self):
        with self.mermaid__edit as _:
            assert type(_)                      is Mermaid__Edit
            assert isinstance(_, MGraph__Edit)  is True
            assert type(_.graph) is Domain__Mermaid__Graph

    def test_add_directive(self):
        with self.mermaid__edit as _:
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.add_directive   ('init: {"flowchart": {"htmlLabels": false}} ')
            _.new_node        (key='markdown', label='This **is** _Markdown_').markdown()

        with self.mermaid__render as _:
            assert _.code() ==  ('%%{init: {"flowchart": {"htmlLabels": false}} }%%\n'
                                 'flowchart LR\n'
                                 '    markdown["`This **is** _Markdown_`"]\n')

    def test_add_edge(self):
        with self.mermaid__edit as _:
            from_node_key    = 'from_key'
            to_node_key      =  'to_key'
            label            = 'an_label'
            edge             = _.add_edge(from_node_key=from_node_key, to_node_key=to_node_key, label=label)
            edge_id          =  edge.edge_config.edge_id
            nodes__by_key    = _.data().nodes__by_key()
            from_node        = nodes__by_key.get(from_node_key)
            to_node          = nodes__by_key.get(to_node_key  )

            assert is_guid(edge_id     ) is True
            assert type(from_node) == Domain__Mermaid__Node
            assert type(from_node) == Domain__Mermaid__Node
            assert type(edge     ) == Domain__Mermaid__Edge

            assert from_node.key         == from_node_key
            assert to_node  .key         == to_node_key
            assert edge.edge.obj() == __(data         =__(label        = label,
                                                          edge_config  = __(edge_id          = edge_id ,
                                                                            output_node_from = False   ,
                                                                            output_node_to   = False   ,
                                                                            edge_mode        = ''      ),
                                                          edge_type    = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge.Schema__Mermaid__Edge',
                                                          edge_data    = __()                           ,
                                                          from_node_id = from_node.node_id              ,
                                                          to_node_id   = to_node.node_id                ))

    def test_add_node(self):
        with self.mermaid__edit as _:
            node        = _.new_node()
            node_id     = node.node_id
            node_key    = node.key
            node_data   = node.node_data
            assert is_guid(node_id)  is True
            assert type(node) is Domain__Mermaid__Node
            assert type(node_key)    is Safe_Id
            assert type(node_data) is Schema__Mermaid__Node__Data
            assert node.obj()        == __(node=__(data=__(key         = node_key            ,
                                                           label       = node_key    ,
                                                           node_data =__(node_shape      = 'default',
                                                                          show_label       = True   ,
                                                                          wrap_with_quotes = True   ,
                                                                          markdown         = False  ,
                                                                          node_id          = node_id),
                                                           node_type   = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node.Schema__Mermaid__Node')),
                                           graph = _.graph.model.obj())

        node_2 = _.new_node(key='an-key', label = 'an-label')
        assert node_2.node.data.obj() == __(key         = 'an-key'                   ,
                                            label       = 'an-label'                 ,
                                            node_data = node_2.node_data.obj() ,
                                            node_type   = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node.Schema__Mermaid__Node')

    def test_render_config(self):
        with Mermaid__Edit().render_config() as _:
            assert type(_) is Schema__Mermaid__Render__Config
            assert _.obj() == __(add_nodes         = True  ,
                                 diagram_direction ='LR'   ,
                                 diagram_type      ='graph',
                                 line_before_edges = True  ,
                                 directives        = []    )

    def test_set_direction(self):
        with self.mermaid__edit as _:
            assert _.set_direction(Schema__Mermaid__Diagram__Direction.LR) is _
            assert _.graph.model.data.render_config.diagram_direction == Schema__Mermaid__Diagram__Direction.LR
            assert _.set_direction('RL') is _
            assert _.graph.model.data.render_config.diagram_direction == Schema__Mermaid__Diagram__Direction.RL