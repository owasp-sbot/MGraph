import pytest
from unittest                                                          import TestCase
from osbot_utils.utils.Misc                                            import list_set
from mgraph_ai.providers.mermaid.models.Model__Mermaid__Node           import Model__Mermaid__Node
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node         import Schema__Mermaid__Node
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Shape  import Schema__Mermaid__Node__Shape
from mgraph_ai.providers.mermaid.Mermaid                               import Mermaid
from mgraph_ai.providers.mermaid.Mermaid__Node                         import Mermaid__Node


class test_Mermaid_Node(TestCase):

    @classmethod
    def setUpClass(cls):
        pytest.skip("todo: fix these tests after MGraph refactoring")

    def setUp(self):
        self.mermaid_node        = Mermaid__Node()
        self.mermaid_node_model  = self.mermaid_node.model
        #self.mermaid_node_data   = self.mermaid_node_model.data
        #self.mermaid_node_config = self.mermaid_node_model.config

    def test__init__(self):
        pass
        # pprint(self.mermaid_node.json())
        # pprint(Model__Mermaid__Node())
        assert type(self.mermaid_node) is Mermaid__Node
        assert list_set(self.mermaid_node.__dict__) == ['model']
        assert type(self.mermaid_node.model) == Model__Mermaid__Node

    def test_shape(self):
        assert self.mermaid_node.shape(Schema__Mermaid__Node__Shape.round_edges).config.node_shape == Schema__Mermaid__Node__Shape.round_edges
        assert self.mermaid_node.shape(Schema__Mermaid__Node__Shape.rhombus    ).config.node_shape == Schema__Mermaid__Node__Shape.rhombus
        assert self.mermaid_node.shape(Schema__Mermaid__Node__Shape.default    ).config.node_shape == Schema__Mermaid__Node__Shape.default
        assert self.mermaid_node.shape('round_edges'                           ).config.node_shape == Schema__Mermaid__Node__Shape.round_edges
        assert self.mermaid_node.shape('rhombus'                               ).config.node_shape == Schema__Mermaid__Node__Shape.rhombus
        assert self.mermaid_node.shape('default'                               ).config.node_shape == Schema__Mermaid__Node__Shape.default
        assert self.mermaid_node.shape('aaaa'                                  ).config.node_shape == Schema__Mermaid__Node__Shape.default
        assert self.mermaid_node.shape(' '                                     ).config.node_shape == Schema__Mermaid__Node__Shape.default
        assert self.mermaid_node.shape(''                                      ).config.node_shape == Schema__Mermaid__Node__Shape.default
        assert self.mermaid_node.shape(None                                    ).config.node_shape == Schema__Mermaid__Node__Shape.default
        assert self.mermaid_node.shape(                                        ).config.node_shape == Schema__Mermaid__Node__Shape.default

    def test_shape__shape_name(self):
        assert self.mermaid_node.shape_hexagon()            is self.mermaid_node;  assert self.mermaid_node.config().node_shape == Schema__Mermaid__Node__Shape.hexagon
        assert self.mermaid_node.shape_parallelogram()      is self.mermaid_node;  assert self.mermaid_node.config().node_shape == Schema__Mermaid__Node__Shape.parallelogram
        assert self.mermaid_node.shape_parallelogram_alt()  is self.mermaid_node;  assert self.mermaid_node.config().node_shape == Schema__Mermaid__Node__Shape.parallelogram_alt
        assert self.mermaid_node.shape_rectangle()          is self.mermaid_node;  assert self.mermaid_node.config().node_shape == Schema__Mermaid__Node__Shape.rectangle
        assert self.mermaid_node.shape_trapezoid()          is self.mermaid_node;  assert self.mermaid_node.config().node_shape == Schema__Mermaid__Node__Shape.trapezoid
        assert self.mermaid_node.shape_trapezoid_alt()      is self.mermaid_node;  assert self.mermaid_node.config().node_shape == Schema__Mermaid__Node__Shape.trapezoid_alt
        assert self.mermaid_node.shape_default()            is self.mermaid_node;  assert self.mermaid_node.config().node_shape == Schema__Mermaid__Node__Shape.default
        assert self.mermaid_node.shape_round_edges()        is self.mermaid_node;  assert self.mermaid_node.config().node_shape == Schema__Mermaid__Node__Shape.round_edges
        assert self.mermaid_node.shape_rhombus()            is self.mermaid_node;  assert self.mermaid_node.config().node_shape == Schema__Mermaid__Node__Shape.rhombus
        assert self.mermaid_node.shape_circle()             is self.mermaid_node;  assert self.mermaid_node.config().node_shape == Schema__Mermaid__Node__Shape.circle


    def test_wrap_with_quotes(self):
        assert self.mermaid_node_config.wrap_with_quotes                         == True
        assert self.mermaid_node.wrap_with_quotes(     ).config.wrap_with_quotes == True
        assert self.mermaid_node.wrap_with_quotes(False).config.wrap_with_quotes == False
        assert self.mermaid_node.wrap_with_quotes(True ).config.wrap_with_quotes == True


    def test__config__wrap_with_quotes(self):
        data_obj = self.mermaid_node_data.set_key('id').set_label('id')
        #model_obj  = self.mermaid_node_model
        node_obj   = self.mermaid_node.wrap_with_quotes()
        assert type(data_obj) is Schema__Mermaid__Node
        assert type(node_obj  ) is Mermaid__Node

        assert node_obj.config().wrap_with_quotes == True
        assert data_obj.key == 'id'

        assert data_obj.json() == dict(attributes  = {}               ,
                                       key         = 'id'             ,
                                       label       = 'id'             ,
                                       node_id     = data_obj.node_id ,
                                       node_type   = None             )
        #assert type_mro(new_node) == [Mermaid__Node, MGraph__Node, Type_Safe, object]

        with Mermaid() as _:
            _.add_node(key='id')
            assert _.code() == 'graph LR\n    id["id"]\n'
            pass
        #pprint(Mermaid().json())

        #return
        with Mermaid() as _:
            _.add_node(key='id').wrap_with_quotes(False)
            assert _.code() == 'graph LR\n    id[id]\n'

        mermaid = Mermaid()
        new_node = mermaid.add_node(key='id')
        new_node.wrap_with_quotes(False)
        assert type(new_node) == Mermaid__Node
        assert new_node.attributes == {}
        assert mermaid.code() == 'graph LR\n    id[id]\n'

