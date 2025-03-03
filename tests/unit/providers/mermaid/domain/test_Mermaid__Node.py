from unittest                                                         import TestCase
from osbot_utils.helpers.Safe_Id                                      import Safe_Id
from osbot_utils.utils.Objects                                        import __
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node        import Schema__Mermaid__Node
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node__Shape import Schema__Mermaid__Node__Shape
from mgraph_db.providers.mermaid.MGraph__Mermaid                      import MGraph__Mermaid
from mgraph_db.providers.mermaid.domain.Domain__Mermaid__Node         import Domain__Mermaid__Node


class test_Mermaid_Node(TestCase):

    def setUp(self):
        self.mermaid_node           = Domain__Mermaid__Node()
        self.mermaid_node_id        = self.mermaid_node.node_id
        self.mermaid_node_data      = self.mermaid_node.node.data

    def test__init__(self):
        with self.mermaid_node as _:
            node_id  = _.node_id
            node_key = _.key
            graph_id = _.graph_id

            assert type(_) is Domain__Mermaid__Node
            assert _.obj() == __(node=__(data=__(key         = node_key                     ,
                                                 label       = node_key                     ,
                                                 node_data =__(node_shape      = 'default',
                                                                show_label       = True     ,
                                                                wrap_with_quotes = True     ,
                                                                markdown         = False    ),
                                                 node_id     = node_id                       ,
                                                 node_type   = 'mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node.Schema__Mermaid__Node'                                            )),
                                 graph=__(data=__(schema_types  = __(edge_type        = 'mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Edge.Schema__Mermaid__Edge'                  ,
                                                                     edge_config_type = 'mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Edge__Config.Schema__Mermaid__Edge__Config'  ,
                                                                     graph_data_type  = 'mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Graph__Config.Schema__Mermaid__Graph__Config',
                                                                     node_type        = 'mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node.Schema__Mermaid__Node'                  ,
                                                                     node_data_type   = 'mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node__Data.Schema__Mermaid__Node__Data'      ),
                                                  edges         = __(),
                                                  graph_data    = __(allow_circle_edges    = False     ,
                                                                     allow_duplicate_edges = False     ,
                                                                     graph_title           = ''       ),
                                                  graph_id      = graph_id                             ,
                                                  graph_type    = 'mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Graph.Schema__Mermaid__Graph',
                                                  mermaid_code  = [],
                                                  nodes         = __(),
                                                  render_config = __(add_nodes         = True   ,
                                                                                         diagram_direction = 'LR'   ,
                                                                                         diagram_type      = 'graph',
                                                                                         line_before_edges = True   ,
                                                                                         directives        = []     )),
                                          model_types = __(node_model_type = 'mgraph_db.providers.mermaid.models.Model__Mermaid__Node.Model__Mermaid__Node',
                                                             edge_model_type = 'mgraph_db.providers.mermaid.models.Model__Mermaid__Edge.Model__Mermaid__Edge')))

    def test_label(self):
        with self.mermaid_node as _:
            assert type(_.label) is Safe_Id
            _.label = Safe_Id('aaa&&!!bbb')
            assert _.label == 'aaa____bbb'
            assert type(_.key) is Safe_Id


    def test_shape(self):
        assert self.mermaid_node.shape(Schema__Mermaid__Node__Shape.round_edges).node_data.node_shape == Schema__Mermaid__Node__Shape.round_edges
        assert self.mermaid_node.shape(Schema__Mermaid__Node__Shape.rhombus    ).node_data.node_shape == Schema__Mermaid__Node__Shape.rhombus
        assert self.mermaid_node.shape(Schema__Mermaid__Node__Shape.default    ).node_data.node_shape == Schema__Mermaid__Node__Shape.default
        assert self.mermaid_node.shape('round_edges'                           ).node_data.node_shape == Schema__Mermaid__Node__Shape.round_edges
        assert self.mermaid_node.shape('rhombus'                               ).node_data.node_shape == Schema__Mermaid__Node__Shape.rhombus
        assert self.mermaid_node.shape('default'                               ).node_data.node_shape == Schema__Mermaid__Node__Shape.default
        assert self.mermaid_node.shape('aaaa'                                  ).node_data.node_shape == Schema__Mermaid__Node__Shape.default
        assert self.mermaid_node.shape(' '                                     ).node_data.node_shape == Schema__Mermaid__Node__Shape.default
        assert self.mermaid_node.shape(''                                      ).node_data.node_shape == Schema__Mermaid__Node__Shape.default
        assert self.mermaid_node.shape(None                                    ).node_data.node_shape == Schema__Mermaid__Node__Shape.default
        assert self.mermaid_node.shape(                                        ).node_data.node_shape == Schema__Mermaid__Node__Shape.default

    def test_shape__shape_name(self):
        assert self.mermaid_node.shape_hexagon()            is self.mermaid_node;  assert self.mermaid_node.node_data.node_shape == Schema__Mermaid__Node__Shape.hexagon
        assert self.mermaid_node.shape_parallelogram()      is self.mermaid_node;  assert self.mermaid_node.node_data.node_shape == Schema__Mermaid__Node__Shape.parallelogram
        assert self.mermaid_node.shape_parallelogram_alt()  is self.mermaid_node;  assert self.mermaid_node.node_data.node_shape == Schema__Mermaid__Node__Shape.parallelogram_alt
        assert self.mermaid_node.shape_rectangle()          is self.mermaid_node;  assert self.mermaid_node.node_data.node_shape == Schema__Mermaid__Node__Shape.rectangle
        assert self.mermaid_node.shape_trapezoid()          is self.mermaid_node;  assert self.mermaid_node.node_data.node_shape == Schema__Mermaid__Node__Shape.trapezoid
        assert self.mermaid_node.shape_trapezoid_alt()      is self.mermaid_node;  assert self.mermaid_node.node_data.node_shape == Schema__Mermaid__Node__Shape.trapezoid_alt
        assert self.mermaid_node.shape_default()            is self.mermaid_node;  assert self.mermaid_node.node_data.node_shape == Schema__Mermaid__Node__Shape.default
        assert self.mermaid_node.shape_round_edges()        is self.mermaid_node;  assert self.mermaid_node.node_data.node_shape == Schema__Mermaid__Node__Shape.round_edges
        assert self.mermaid_node.shape_rhombus()            is self.mermaid_node;  assert self.mermaid_node.node_data.node_shape == Schema__Mermaid__Node__Shape.rhombus
        assert self.mermaid_node.shape_circle()             is self.mermaid_node;  assert self.mermaid_node.node_data.node_shape == Schema__Mermaid__Node__Shape.circle


    def test_wrap_with_quotes(self):
        assert self.mermaid_node_data.node_data.wrap_with_quotes                    == True
        assert self.mermaid_node.wrap_with_quotes(     ).node_data.wrap_with_quotes == True
        assert self.mermaid_node.wrap_with_quotes(False).node_data.wrap_with_quotes == False
        assert self.mermaid_node.wrap_with_quotes(True ).node_data.wrap_with_quotes == True


    def test__config__wrap_with_quotes(self):
        data_obj  = self.mermaid_node_data
        data_obj.key   = Safe_Id('id')
        data_obj.label = 'id'
        node_obj  = self.mermaid_node.wrap_with_quotes()
        assert type(data_obj ) is Schema__Mermaid__Node
        assert type(node_obj ) is Domain__Mermaid__Node

        assert node_obj.node_data.wrap_with_quotes == True
        assert data_obj.key == 'id'

        assert data_obj.obj() == __(key         = 'id',
                                    label       = 'id',
                                    node_data = __(node_shape       = 'default',
                                                     show_label       = True,
                                                     wrap_with_quotes = True,
                                                     markdown         = False),
                                   node_id      = self.mermaid_node_id        ,
                                   node_type    = 'mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node.Schema__Mermaid__Node')
        assert Schema__Mermaid__Node.from_json(data_obj.json()).json() == data_obj.json()

        with MGraph__Mermaid() as _:
            _.edit().new_node(key=Safe_Id('id'))
            assert _.code() == 'graph LR\n    id["id"]\n'

        #return
        with MGraph__Mermaid() as _:
            _.edit().new_node(key=Safe_Id('id')).wrap_with_quotes(False)
            assert _.code() == 'graph LR\n    id[id]\n'

        mermaid = MGraph__Mermaid()
        new_node = mermaid.edit().new_node(key=Safe_Id('id'))
        new_node.wrap_with_quotes(False)

        assert type(new_node) == Domain__Mermaid__Node
        assert mermaid.code() == 'graph LR\n    id[id]\n'

    def test_new_node(self):
        key_value = Safe_Id('this-is-an-key')
        with MGraph__Mermaid() as _:
            assert _.edit().new_node(key=key_value).key == key_value
            assert _.render().code() == f'graph LR\n    {key_value}["{key_value}"]\n'