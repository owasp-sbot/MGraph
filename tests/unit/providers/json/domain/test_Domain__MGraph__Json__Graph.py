from unittest                                                       import TestCase
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config          import Schema__MGraph__Edge__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph__Data           import Schema__MGraph__Graph__Data
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data            import Schema__MGraph__Node__Data
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Edge     import Domain__MGraph__Json__Edge
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node     import Domain__MGraph__Json__Node
from mgraph_ai.providers.json.models.Model__MGraph__Json__Edge      import Model__MGraph__Json__Edge
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node      import Model__MGraph__Json__Node
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Edge    import Schema__MGraph__Json__Edge
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Graph   import Schema__MGraph__Json__Graph
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node    import Schema__MGraph__Json__Node
from osbot_utils.utils.Objects                                      import __, full_type_name
from mgraph_ai.mgraph.domain.Domain__MGraph__Graph                  import Domain__MGraph__Graph
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Graph    import Domain__MGraph__Json__Graph


class test_Domain__MGraph__Json__Graph(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.domain_graph = Domain__MGraph__Json__Graph()

    def test__init__(self):
        with self.domain_graph as _:
            assert isinstance(_, Domain__MGraph__Graph)
            assert _.obj() == __(domain_types = __(node_domain_type = full_type_name(Domain__MGraph__Json__Node),
                                                   edge_domain_type = full_type_name(Domain__MGraph__Json__Edge)),
                                 model        = __(data             = __(schema_types    = __(edge_type        = full_type_name(Schema__MGraph__Json__Edge   ),
                                                                                              edge_config_type = full_type_name(Schema__MGraph__Edge__Config ),
                                                                                              graph_data_type  = full_type_name(Schema__MGraph__Graph__Data  ),
                                                                                              node_type        = full_type_name(Schema__MGraph__Json__Node   ),
                                                                                              node_data_type   = full_type_name(Schema__MGraph__Node__Data   )),
                                                                         edges           = __(),
                                                                         graph_data      = __(),
                                                                         graph_id        = _.graph_id(),
                                                                         graph_type      = full_type_name(Schema__MGraph__Json__Graph),
                                                                         nodes           = __()),
                                                  model_types       = __(node_model_type = full_type_name(Model__MGraph__Json__Node),
                                                                         edge_model_type = full_type_name(Model__MGraph__Json__Edge)))) != __()

    def test_new_node(self):
        with self.domain_graph.new_node() as _:
            assert type(_) is Domain__MGraph__Json__Node

    def test_new_edge(self):
        node_1 = self.domain_graph.new_node()
        node_2 = self.domain_graph.new_node()
        assert type(node_1) is Domain__MGraph__Json__Node
        assert type(node_2) is Domain__MGraph__Json__Node
        with self.domain_graph.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id) as _:
            assert type(_) is Domain__MGraph__Json__Edge
            assert type(_.from_node()) == Domain__MGraph__Json__Node
            assert type(_.to_node  ()) == Domain__MGraph__Json__Node
            assert _.from_node_id()    == node_1.node_id
            assert _.to_node_id  ()  == node_2.node_id



