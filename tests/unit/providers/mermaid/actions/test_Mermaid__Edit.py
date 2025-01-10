from unittest                                                           import TestCase
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Config  import Schema__Mermaid__Node__Config
from osbot_utils.helpers.Safe_Id                                        import Safe_Id
from osbot_utils.utils.Objects                                          import __
from mgraph_ai.providers.mermaid.domain.Mermaid__Node                   import Mermaid__Node
from osbot_utils.utils.Misc                                             import is_guid
from mgraph_ai.mgraph.actions.MGraph__Edit                              import MGraph__Edit
from mgraph_ai.providers.mermaid.actions.Mermaid__Edit                  import Mermaid__Edit
from mgraph_ai.providers.mermaid.domain.Mermaid__Graph                  import Mermaid__Graph


class test__Mermaid__Edit(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mermaid__edit = Mermaid__Edit()

    def test__init__(self):
        with self.mermaid__edit as _:
            assert type(_)                      is Mermaid__Edit
            assert isinstance(_, MGraph__Edit)  is True
            assert type(_.graph)                is Mermaid__Graph

    def test_add_node(self):
        with self.mermaid__edit as _:
            node        = _.add_node()
            node_id     = node.node_id()
            node_key    = node.node_key()
            node_config = node.node_config()
            assert is_guid(node_id)  is True
            assert type(node)        is Mermaid__Node
            assert type(node_key)    is Safe_Id
            assert type(node_config) is Schema__Mermaid__Node__Config
            assert node.obj()        == __(node=__(data=__(key         = node_key            ,
                                                           label       = node_key    ,
                                                           node_config =__(node_shape      = 'default',
                                                                          show_label       = True,
                                                                          wrap_with_quotes = True,
                                                                          markdown         = False,
                                                                          value_type       = None,
                                                                          node_id          = node_id),
                                                           node_type   = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node.Schema__Mermaid__Node',
                                                           attributes  =__() ,
                                                           value       =None )),
                                           graph = _.graph.model.obj())

        node_2 = _.add_node(key='an-key', value='an-value', label = 'an-label')
        assert node_2.node.data.obj() == __(key         = 'an-key'                   ,
                                            label       = 'an-label'                 ,
                                            node_config = node_2.node_config().obj() ,
                                            node_type   = 'mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node.Schema__Mermaid__Node',
                                            attributes  = __()                       ,
                                            value       = 'an-value'                 )