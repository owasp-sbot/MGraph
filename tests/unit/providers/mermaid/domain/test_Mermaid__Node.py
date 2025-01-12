from unittest                                                          import TestCase
from osbot_utils.helpers.Safe_Id                                       import Safe_Id
from osbot_utils.utils.Objects                                         import __
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node         import Schema__Mermaid__Node
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Shape  import Schema__Mermaid__Node__Shape
from mgraph_ai.providers.mermaid.domain.Mermaid                        import Mermaid
from mgraph_ai.providers.mermaid.domain.Mermaid__Node                  import Mermaid__Node


class test_Mermaid_Node(TestCase):

    def setUp(self):
        self.mermaid_node        = Mermaid__Node()
        self.mermaid_node_id     = self.mermaid_node.node_id
        self.mermaid_node_data   = self.mermaid_node.node.data
        self.mermaid_node_config = self.mermaid_node.node.data.node_config

    def test__init__(self):
        with self.mermaid_node as _:
            node_id  = _.node_id
            node_key = _.key
            graph_id = _.graph_id

            assert type(_) is Mermaid__Node
            assert _.obj() == __(node=__(data=__(key         = node_key                     ,
                                                 label       = node_key                     ,
                                                 node_config =__(node_shape      = 'default',
                                                                show_label       = True     ,
                                                                wrap_with_quotes = True     ,
                                                                markdown         = False    ,
                                                                node_id          = node_id  ,
                                                                value_type       = None     ),
                                                 node_type   = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node.Schema__Mermaid__Node',
                                                 attributes  = __(),
                                                 value=None)),
                                 graph=__(data=__(default_types = __(edge_type         = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge.Schema__Mermaid__Edge',
                                                                     edge_config_type  = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge__Config.Schema__Mermaid__Edge__Config',
                                                                     graph_config_type = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Graph__Config.Schema__Mermaid__Graph__Config',
                                                                     node_type         = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node.Schema__Mermaid__Node',
                                                                     node_config_type  = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Config.Schema__Mermaid__Node__Config',
                                                                     attribute_type    = 'mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute.Schema__MGraph__Attribute'),
                                                  edges         = __(),
                                                  graph_config  = __(allow_circle_edges    = False     ,
                                                                     allow_duplicate_edges = False     ,
                                                                     graph_title           = ''       ,
                                                                     graph_id              = graph_id ),
                                                  graph_type    = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Graph.Schema__Mermaid__Graph',
                                                  mermaid_code  = [],
                                                  nodes         = __(),
                                                  render_config = __(add_nodes         = True   ,
                                                                                         diagram_direction = 'LR'   ,
                                                                                         diagram_type      = 'graph',
                                                                                         line_before_edges = True   ,
                                                                                         directives        = []     )),
                                          node_model_type = 'mgraph_ai.providers.mermaid.models.Model__Mermaid__Node.Model__Mermaid__Node',
                                          edge_model_type = 'mgraph_ai.providers.mermaid.models.Model__Mermaid__Edge.Model__Mermaid__Edge'))

    def test_label(self):
        with self.mermaid_node as _:
            assert type(_.label) is Safe_Id
            _.label = Safe_Id('aaa&&!!bbb')
            assert _.label == 'aaa____bbb'
            assert type(_.key) is Safe_Id


    def test_shape(self):
        assert self.mermaid_node.shape(Schema__Mermaid__Node__Shape.round_edges).node_config.node_shape == Schema__Mermaid__Node__Shape.round_edges
        assert self.mermaid_node.shape(Schema__Mermaid__Node__Shape.rhombus    ).node_config.node_shape == Schema__Mermaid__Node__Shape.rhombus
        assert self.mermaid_node.shape(Schema__Mermaid__Node__Shape.default    ).node_config.node_shape == Schema__Mermaid__Node__Shape.default
        assert self.mermaid_node.shape('round_edges'                           ).node_config.node_shape == Schema__Mermaid__Node__Shape.round_edges
        assert self.mermaid_node.shape('rhombus'                               ).node_config.node_shape == Schema__Mermaid__Node__Shape.rhombus
        assert self.mermaid_node.shape('default'                               ).node_config.node_shape == Schema__Mermaid__Node__Shape.default
        assert self.mermaid_node.shape('aaaa'                                  ).node_config.node_shape == Schema__Mermaid__Node__Shape.default
        assert self.mermaid_node.shape(' '                                     ).node_config.node_shape == Schema__Mermaid__Node__Shape.default
        assert self.mermaid_node.shape(''                                      ).node_config.node_shape == Schema__Mermaid__Node__Shape.default
        assert self.mermaid_node.shape(None                                    ).node_config.node_shape == Schema__Mermaid__Node__Shape.default
        assert self.mermaid_node.shape(                                        ).node_config.node_shape == Schema__Mermaid__Node__Shape.default

    def test_shape__shape_name(self):
        assert self.mermaid_node.shape_hexagon()            is self.mermaid_node;  assert self.mermaid_node.node_config.node_shape == Schema__Mermaid__Node__Shape.hexagon
        assert self.mermaid_node.shape_parallelogram()      is self.mermaid_node;  assert self.mermaid_node.node_config.node_shape == Schema__Mermaid__Node__Shape.parallelogram
        assert self.mermaid_node.shape_parallelogram_alt()  is self.mermaid_node;  assert self.mermaid_node.node_config.node_shape == Schema__Mermaid__Node__Shape.parallelogram_alt
        assert self.mermaid_node.shape_rectangle()          is self.mermaid_node;  assert self.mermaid_node.node_config.node_shape == Schema__Mermaid__Node__Shape.rectangle
        assert self.mermaid_node.shape_trapezoid()          is self.mermaid_node;  assert self.mermaid_node.node_config.node_shape == Schema__Mermaid__Node__Shape.trapezoid
        assert self.mermaid_node.shape_trapezoid_alt()      is self.mermaid_node;  assert self.mermaid_node.node_config.node_shape == Schema__Mermaid__Node__Shape.trapezoid_alt
        assert self.mermaid_node.shape_default()            is self.mermaid_node;  assert self.mermaid_node.node_config.node_shape == Schema__Mermaid__Node__Shape.default
        assert self.mermaid_node.shape_round_edges()        is self.mermaid_node;  assert self.mermaid_node.node_config.node_shape == Schema__Mermaid__Node__Shape.round_edges
        assert self.mermaid_node.shape_rhombus()            is self.mermaid_node;  assert self.mermaid_node.node_config.node_shape == Schema__Mermaid__Node__Shape.rhombus
        assert self.mermaid_node.shape_circle()             is self.mermaid_node;  assert self.mermaid_node.node_config.node_shape == Schema__Mermaid__Node__Shape.circle


    def test_wrap_with_quotes(self):
        assert self.mermaid_node_config.wrap_with_quotes                         == True
        assert self.mermaid_node.wrap_with_quotes(     ).node_config.wrap_with_quotes == True
        assert self.mermaid_node.wrap_with_quotes(False).node_config.wrap_with_quotes == False
        assert self.mermaid_node.wrap_with_quotes(True ).node_config.wrap_with_quotes == True


    def test__config__wrap_with_quotes(self):
        data_obj  = self.mermaid_node_data
        data_obj.key   = 'id'
        data_obj.label = 'id'
        node_obj  = self.mermaid_node.wrap_with_quotes()
        assert type(data_obj ) is Schema__Mermaid__Node
        assert type(node_obj ) is Mermaid__Node

        assert node_obj.node_config.wrap_with_quotes == True
        assert data_obj.key == 'id'

        assert data_obj.obj() == __(key         = 'id',
                                    label       = 'id',
                                    node_config = __(node_shape       = 'default',
                                                     show_label       = True,
                                                     wrap_with_quotes = True,
                                                     markdown         = False,
                                                     node_id          = self.mermaid_node_id,
                                                     value_type       = None                ),
                                   node_type    = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node.Schema__Mermaid__Node',
                                   attributes   = __(),
                                   value=None)
        assert Schema__Mermaid__Node.from_json(data_obj.json()).json() == data_obj.json()
        #pprint(node_obj.json())


        with Mermaid() as _:
            _.edit().new_node(key='id')
            assert _.code() == 'graph LR\n    id["id"]\n'




        #return
        with Mermaid() as _:
            _.edit().new_node(key='id').wrap_with_quotes(False)
            assert _.code() == 'graph LR\n    id[id]\n'

        mermaid = Mermaid()
        new_node = mermaid.edit().new_node(key='id')
        new_node.wrap_with_quotes(False)

        assert type(new_node) == Mermaid__Node
        assert new_node.attributes() == []
        assert mermaid.code() == 'graph LR\n    id[id]\n'

    def test_new_node(self):
        key_value = 'this-is-an-key'
        with Mermaid() as _:
            assert _.edit().new_node(key=key_value).key == key_value
            assert _.render().code() == f'graph LR\n    {key_value}["{key_value}"]\n'