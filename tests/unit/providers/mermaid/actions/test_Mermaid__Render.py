import pytest
from unittest                                                               import TestCase
from osbot_utils.utils.Objects                                              import __
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Diagram_Direction import Schema__Mermaid__Diagram__Direction
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Diagram__Type     import Schema__Mermaid__Diagram__Type
from mgraph_ai.providers.mermaid.configs.Mermaid__Render__Config            import Mermaid__Render__Config
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Shape       import Schema__Mermaid__Node__Shape
from mgraph_ai.providers.mermaid.domain.Mermaid                             import Mermaid
from osbot_utils.testing.Stdout                                             import Stdout
from osbot_utils.utils.Str                                                  import str_dedent

class test_Mermaid__Render(TestCase):

    @classmethod
    def setUpClass(cls):
        pytest.skip("todo: fix these tests after MGraph refactoring")

    def setUp(self):
        self.mermaid        = Mermaid()
        self.mermaid_render = self.mermaid.render()
        self.mermaid_edit   = self.mermaid.edit()

    def test__init__(self):
        with self.mermaid_render as _:
            expected_data = __(config            = _.config.obj(),
                               diagram_direction = Schema__Mermaid__Diagram__Direction.LR.value,
                               diagram_type      = Schema__Mermaid__Diagram__Type.graph  .value,
                               graph             = _.graph.obj(),
                               mermaid_code      = [])
            assert _              is not None
            assert _.obj()        == expected_data
            assert type(_.config) is Mermaid__Render__Config



    def test_code(self):
        expected_code = str_dedent("""
                                        flowchart TD
                                            A[Christmas] -->|Get money| B(Go shopping)
                                            B --> C{Let me think}
                                            C -->|One| D[Laptop]
                                            C -->|Two| E[iPhone]
                                            C -->|Three| F[fa:fa-car Car]
                                            """)

        with self.mermaid as _:
            _.render().config.add_nodes         = False
            _.render().config.line_before_edges = False
            _.set_direction(Schema__Mermaid__Diagram__Direction.TD)
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.add_node(key='A').set_label('Christmas'    ).wrap_with_quotes(False).shape_default    ()
            _.add_node(key='B').set_label('Go shopping'  ).wrap_with_quotes(False).shape_round_edges()
            _.add_node(key='C').set_label('Let me think' ).wrap_with_quotes(False).shape_rhombus    ()
            _.add_node(key='D').set_label('Laptop'       ).wrap_with_quotes(False)
            _.add_node(key='E').set_label('iPhone'       ).wrap_with_quotes(False)
            _.add_node(key='F').set_label('fa:fa-car Car').wrap_with_quotes(False)
            _.add_edge('A', 'B', label='Get money').output_node_from().output_node_to().edge_mode__lr_using_pipe()
            _.add_edge('B', 'C'                   ).output_node_to()
            _.add_edge('C', 'D', label='One'      ).output_node_to().edge_mode__lr_using_pipe()
            _.add_edge('C', 'E', label='Two'      ).output_node_to().edge_mode__lr_using_pipe()
            _.add_edge('C', 'F', label='Three'    ).output_node_to().edge_mode__lr_using_pipe()

            assert expected_code ==_.code()
            #file_path = self.mermaid.save()

            assert expected_code == _.code()
            with Stdout() as stdout:
                _.print_code()
            assert stdout.value() == expected_code + '\n'
            assert _.render().mermaid_code == expected_code.splitlines()

            _.render().reset_code()
            assert _.render().mermaid_code == []

            assert expected_code == _.code()

    def test_code__more_cases(self):
        with self.mermaid as _:
            _.add_directive('init: {"flowchart": {"htmlLabels": false}} ')
            assert _.code() == ('%%{init: {"flowchart": {"htmlLabels": false}} }%%\n'
                                'graph LR\n')

            _.add_node(key='markdown', label='This **is** _Markdown_').markdown()

            _.render().code_create(_.nodes(), _.edges(), recreate=True)
            assert _.code() == ('%%{init: {"flowchart": {"htmlLabels": false}} }%%\n'
                                'graph LR\n'
                                '    markdown["`This **is** _Markdown_`"]\n')

            assert self.mermaid_render.diagram_type == Schema__Mermaid__Diagram__Type.graph

    def test_print_code(self):
        with self.mermaid_edit as _:
            _.add_edge(from_node_key='from_node', to_node_key='to_node')
        with self.mermaid_render as _:
            with Stdout() as stdout:
                _.print_code()
        assert stdout.value() == ('graph LR\n'
                                  '    from_node["from_node"]\n'
                                  '    to_node["to_node"]\n'
                                  '\n'
                                  '    from_node --> to_node\n')

    def test_render_edge(self):
        with self.mermaid_edit as _:
            mermaid_edge = _.new_edge()
        return
        render_edge  = self.mermaid_render.render_edge
        from_node_id = self.mermaid_edge.from_node_id
        to_node_id   = self.mermaid_edge.to_node_id
        from_node    = self.mermaid.graph.node(from_node_id)
        to_node      = self.mermaid.graph.node(to_node_id  )
        assert render_edge(self.mermaid_edge) == f'    {from_node.key} --> {to_node.key}'
        from_node.label = 'from node'
        to_node.label   = 'to node'
        assert render_edge(self.mermaid_edge) == f'    {from_node.key} --> {to_node.key}'
        self.mermaid_edge.label = 'link_type'
        assert render_edge(self.mermaid_edge) == f'    {from_node.key} --"{self.mermaid_edge.label}"--> {to_node.key}'
        self.mermaid_edge.edge_mode__lr_using_pipe()
        assert render_edge(self.mermaid_edge) == f'    {from_node.key} -->|{self.mermaid_edge.label}| {to_node.key}'
        self.mermaid_edge.output_node_to()
        assert render_edge(self.mermaid_edge) == f'    {from_node.key} -->|{self.mermaid_edge.label}| {to_node.key}["to node"]'

    def test__render_node__node_shape(self):
        render_node = self.mermaid_render.render_node
        with self.mermaid.add_node(key='id') as _:
            assert render_node(_                                                ) == '    id["id"]'
            assert render_node(_.shape(''                                      )) == '    id["id"]'
            assert render_node(_.shape('aaaaa'                                 )) == '    id["id"]'
            assert render_node(_.shape('round_edges'                           )) == '    id("id")'
            assert render_node(_.shape('rhombus'                               )) == '    id{"id"}'
            assert render_node(_.shape(Schema__Mermaid__Node__Shape.default    )) == '    id["id"]'
            assert render_node(_.shape(Schema__Mermaid__Node__Shape.rectangle  )) == '    id["id"]'
            assert render_node(_.shape(Schema__Mermaid__Node__Shape.round_edges)) == '    id("id")'
            assert render_node(_.shape(Schema__Mermaid__Node__Shape.rhombus    )) == '    id{"id"}'



