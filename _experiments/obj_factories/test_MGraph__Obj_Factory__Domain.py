from unittest                                                       import TestCase
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge                  import Schema__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config          import Schema__MGraph__Edge__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph                 import Schema__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph__Data           import Schema__MGraph__Graph__Data
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node                  import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data            import Schema__MGraph__Node__Data
from osbot_utils.testing.performance.Performance_Measure__Session   import Performance_Measure__Session
from osbot_utils.utils.Objects                                      import __, type_full_name
from mgraph_ai.mgraph.actions.MGraph__Obj_Factory__Domain           import MGraph__Obj_Factory__Domain
from mgraph_ai.mgraph.domain.Domain__MGraph__Edge                   import Domain__MGraph__Edge
from mgraph_ai.mgraph.domain.Domain__MGraph__Graph                  import Domain__MGraph__Graph
from mgraph_ai.mgraph.domain.Domain__MGraph__Node                   import Domain__MGraph__Node
from mgraph_ai.mgraph.domain.Domain__MGraph__Types                  import Domain__MGraph__Types
from mgraph_ai.mgraph.models.Model__MGraph__Edge                    import Model__MGraph__Edge
from mgraph_ai.mgraph.models.Model__MGraph__Graph                   import Model__MGraph__Graph
from mgraph_ai.mgraph.models.Model__MGraph__Node                    import Model__MGraph__Node

class test_MGraph__Obj_Factory__Domain(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.assert_enabled = False
        cls.session        = Performance_Measure__Session(assert_enabled=cls.assert_enabled)
        cls.domain_factory = MGraph__Obj_Factory__Domain()

    def test_create_all_objects(self):
        with self.session as _:
            print()
            print()
            _.padding = 36
            _.measure(self.domain_factory.create__Domain__MGraph__Types).print().assert_time__less_than(500)
            _.measure(self.domain_factory.create__Domain__MGraph__Node ).print().assert_time__less_than(5000)
            _.measure(self.domain_factory.create__Domain__MGraph__Edge ).print().assert_time__less_than(7000)
            _.measure(self.domain_factory.create__Domain__MGraph__Graph).print().assert_time__less_than(4000)
            print()
            _.measure(Domain__MGraph__Types).print()
            _.measure(Domain__MGraph__Node ).print()
            _.measure(Domain__MGraph__Edge ).print()
            _.measure(Domain__MGraph__Graph).print()

    def test_create__Domain__MGraph__Types(self):
        types = self.domain_factory.create__Domain__MGraph__Types()
        with types as _:
            assert type(_)               is Domain__MGraph__Types
            assert _.node_domain_type    is Domain__MGraph__Node
            assert _.edge_domain_type    is Domain__MGraph__Edge
            assert _.obj()               == __(node_domain_type = type_full_name(Domain__MGraph__Node),
                                               edge_domain_type = type_full_name(Domain__MGraph__Edge))

    def test_create__Domain__MGraph__Node(self):
        node = self.domain_factory.create__Domain__MGraph__Node()
        with node as _:
            assert type(_)        is Domain__MGraph__Node
            assert type(_.node)   is Model__MGraph__Node
            assert type(_.graph)  is Model__MGraph__Graph
            assert _.obj()        == __(node = __(data = __(node_data = __(),
                                                            node_id   = _.node.data.node_id,
                                                            node_type = type_full_name(Schema__MGraph__Node))),
                                       graph = __(data = __(edges        = __(),
                                                            graph_data   = __(),
                                                            graph_id     = _.graph.data.graph_id,
                                                            graph_type   = type_full_name(Schema__MGraph__Graph),
                                                            nodes        = __(),
                                                            schema_types = __(edge_type        = type_full_name(Schema__MGraph__Edge        ),
                                                                              edge_config_type = type_full_name(Schema__MGraph__Edge__Config),
                                                                              graph_data_type  = type_full_name(Schema__MGraph__Graph__Data ),
                                                                              node_type        = type_full_name(Schema__MGraph__Node        ),
                                                                              node_data_type   = type_full_name(Schema__MGraph__Node__Data))),
                                                  model_types = __(node_model_type = type_full_name(Model__MGraph__Node),
                                                                  edge_model_type  = type_full_name(Model__MGraph__Edge))))

    def test_create__Domain__MGraph__Edge(self):
        edge = self.domain_factory.create__Domain__MGraph__Edge()
        with edge as _:
            assert type(_)        is Domain__MGraph__Edge
            assert type(_.edge)   is Model__MGraph__Edge
            assert type(_.graph)  is Model__MGraph__Graph
            assert _.obj()        == __(edge = __(data = __(edge_config  = __(edge_id = _.edge.data.edge_config.edge_id),
                                                            edge_data    = __(),
                                                            edge_type    = type_full_name(Schema__MGraph__Edge),
                                                            from_node_id = _.edge.data.from_node_id,
                                                            to_node_id   = _.edge.data.to_node_id)),
                                        graph = __(data = __(edges       = __(),
                                                            graph_data   = __(),
                                                            graph_id     = _.graph.data.graph_id,
                                                            graph_type   = type_full_name(Schema__MGraph__Graph),
                                                            nodes        = __(),
                                                            schema_types = __(edge_type        = type_full_name(Schema__MGraph__Edge),
                                                                              edge_config_type = type_full_name(Schema__MGraph__Edge__Config),
                                                                              graph_data_type  = type_full_name(Schema__MGraph__Graph__Data),
                                                                              node_type        = type_full_name(Schema__MGraph__Node),
                                                                              node_data_type   = type_full_name(Schema__MGraph__Node__Data))),
                                                   model_types = __(node_model_type = type_full_name(Model__MGraph__Node),
                                                                    edge_model_type = type_full_name(Model__MGraph__Edge))))

    def test_create__Domain__MGraph__Graph(self):
        graph = self.domain_factory.create__Domain__MGraph__Graph()
        with graph as _:
            assert type(_)               is Domain__MGraph__Graph
            assert type(_.domain_types)  is Domain__MGraph__Types
            assert type(_.model)         is Model__MGraph__Graph
            assert _.obj()               == __(domain_types = __(node_domain_type = type_full_name(Domain__MGraph__Node),
                                                                 edge_domain_type = type_full_name(Domain__MGraph__Edge)),
                                               model = __(data = __(edges        = __(),
                                                                    graph_data   = __(),
                                                                    graph_id     = _.model.data.graph_id,
                                                                    graph_type   = type_full_name(Schema__MGraph__Graph),
                                                                    nodes        = __(),
                                                                    schema_types = __(edge_type        = type_full_name(Schema__MGraph__Edge),
                                                                                      edge_config_type = type_full_name(Schema__MGraph__Edge__Config),
                                                                                      graph_data_type  = type_full_name(Schema__MGraph__Graph__Data),
                                                                                      node_type        = type_full_name(Schema__MGraph__Node),
                                                                                      node_data_type   = type_full_name(Schema__MGraph__Node__Data))),
                                                          model_types = __(node_model_type = type_full_name(Model__MGraph__Node),
                                                                           edge_model_type = type_full_name(Model__MGraph__Edge))))