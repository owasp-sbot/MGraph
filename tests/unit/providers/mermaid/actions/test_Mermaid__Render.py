from unittest                                                               import TestCase
from osbot_utils.utils.Files                                                import file_exists
from mgraph_ai.providers.mermaid.domain.Mermaid__Edge                       import Mermaid__Edge
from mgraph_ai.providers.mermaid.domain.Mermaid__Node                       import Mermaid__Node
from osbot_utils.utils.Objects                                              import __
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Diagram_Direction import Schema__Mermaid__Diagram__Direction
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Diagram__Type     import Schema__Mermaid__Diagram__Type
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Shape       import Schema__Mermaid__Node__Shape
from mgraph_ai.providers.mermaid.domain.Mermaid                             import Mermaid
from osbot_utils.testing.Stdout                                             import Stdout
from osbot_utils.utils.Str                                                  import str_dedent

class test_Mermaid__Render(TestCase):

    def setUp(self):
        self.mermaid        = Mermaid()
        self.mermaid_render = self.mermaid.render()
        self.mermaid_edit   = self.mermaid.edit()
        self.mermaid_data   = self.mermaid.data()

    def test__init__(self):
        with self.mermaid_render as _:
            expected_data = __(graph             = _.graph.obj(),
                               mermaid_code      = [])
            assert _              is not None
            assert _.obj()        == expected_data



    def test_code(self):
        expected_code = str_dedent("""
                                        flowchart TD
                                            A[Christmas] -->|Get money| B(Go shopping)
                                            B --> C{Let me think}
                                            C -->|One| D[Laptop]
                                            C -->|Two| E[iPhone]
                                            C -->|Three| F[fa:fa-car Car]
                                            """)


        with self.mermaid_edit as _:
            _.render_config().add_nodes         = False
            _.render_config().line_before_edges = False
            _.set_direction(Schema__Mermaid__Diagram__Direction.TD)
            _.set_diagram_type(Schema__Mermaid__Diagram__Type.flowchart)
            _.new_node(key='A', label='Christmas'    ).wrap_with_quotes(False).shape_default    ()
            _.new_node(key='B').set_label('Go shopping'  ).wrap_with_quotes(False).shape_round_edges()
            _.new_node(key='C').set_label('Let me think' ).wrap_with_quotes(False).shape_rhombus    ()
            _.new_node(key='D').set_label('Laptop'       ).wrap_with_quotes(False)
            _.new_node(key='E').set_label('iPhone'       ).wrap_with_quotes(False)
            _.new_node(key='F').set_label('fa:fa-car Car').wrap_with_quotes(False)
            _.add_edge('A', 'B', label='Get money').output_node_from().output_node_to().edge_mode__lr_using_pipe()
            _.add_edge('B', 'C'                   ).output_node_to()
            _.add_edge('C', 'D', label='One'      ).output_node_to().edge_mode__lr_using_pipe()
            _.add_edge('C', 'E', label='Two'      ).output_node_to().edge_mode__lr_using_pipe()
            _.add_edge('C', 'F', label='Three'    ).output_node_to().edge_mode__lr_using_pipe()

        with self.mermaid_render as _:
            file_path = _.save()

            assert file_exists(file_path) is True
            assert expected_code          == _.code()

            with Stdout() as stdout:
                _.print_code()

            assert stdout.value() == expected_code + '\n'
            assert _.mermaid_code == expected_code.splitlines()

            _.reset_code()
            assert _.mermaid_code  == []
            assert expected_code   == _.code()
            assert _.mermaid_code  != []

    def test_code__more_cases(self):
        with self.mermaid_edit as _:
            _.add_directive('init: {"flowchart": {"htmlLabels": false}} ')
            # assert _.code() == ('%%{init: {"flowchart": {"htmlLabels": false}} }%%\n'
            #                     'graph LR\n')

            self.mermaid_render.code()
            _.new_node(key='markdown', label='This **is** _Markdown_').markdown()

            self.mermaid_render.code_create(recreate=True)

            #return

            assert self.mermaid_render.code() == ('%%{init: {"flowchart": {"htmlLabels": false}} }%%\n'
                                                  'graph LR\n'
                                                  '    markdown["`This **is** _Markdown_`"]\n')

            assert self.mermaid_render.config().diagram_type == Schema__Mermaid__Diagram__Type.graph

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
        render_edge = self.mermaid_render.render_edge                               # helper method to make the code more readable
        with self.mermaid_edit as _:
            mermaid_edge = _.new_edge()
            from_node_id = mermaid_edge.from_node_id()
            to_node_id   = mermaid_edge.to_node_id()
            from_node    = self.mermaid_data.node(from_node_id)
            to_node      = self.mermaid_data.node(to_node_id  )

            assert type(mermaid_edge)        is Mermaid__Edge
            assert self.mermaid_render.graph == _.graph                             # make sure these are the same
            assert type(from_node)           is Mermaid__Node
            assert type(to_node)             is Mermaid__Node
            assert render_edge(mermaid_edge) == f'    {from_node.node_key()} --> {to_node.node_key()}'

        with self.mermaid_edit as _:

            from_node.label = 'from node'
            to_node  .label = 'to node'
            assert render_edge(mermaid_edge) == f'    {from_node.key} --> {to_node.key}'
            mermaid_edge.label = 'link_type'

            assert render_edge(mermaid_edge) == f'    {from_node.key} --"{mermaid_edge.label}"--> {to_node.key}'
            mermaid_edge.edge_mode__lr_using_pipe()
            assert render_edge(mermaid_edge) == f'    {from_node.key} -->|{mermaid_edge.label}| {to_node.key}'
            mermaid_edge.output_node_to()
            assert render_edge(mermaid_edge) == f'    {from_node.key} -->|{mermaid_edge.label}| {to_node.key}["to node"]'

    def test__render_node__node_shape(self):
        render_node = self.mermaid_render.render_node
        with self.mermaid_edit.new_node(key='id') as _:
            assert render_node(_                                                ) == '    id["id"]'
            assert render_node(_.shape(''                                      )) == '    id["id"]'
            assert render_node(_.shape('aaaaa'                                 )) == '    id["id"]'
            assert render_node(_.shape('round_edges'                           )) == '    id("id")'
            assert render_node(_.shape('rhombus'                               )) == '    id{"id"}'
            assert render_node(_.shape(Schema__Mermaid__Node__Shape.default    )) == '    id["id"]'
            assert render_node(_.shape(Schema__Mermaid__Node__Shape.rectangle  )) == '    id["id"]'
            assert render_node(_.shape(Schema__Mermaid__Node__Shape.round_edges)) == '    id("id")'
            assert render_node(_.shape(Schema__Mermaid__Node__Shape.rhombus    )) == '    id{"id"}'



