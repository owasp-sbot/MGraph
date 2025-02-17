from unittest                                               import TestCase
from mgraph_db.mgraph.MGraph                                import MGraph
from mgraph_db.mgraph.domain.Domain__MGraph__Graph          import Domain__MGraph__Graph
from mgraph_db.mgraph.models.Model__MGraph__Graph           import Model__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value   import Schema__MGraph__Node__Value
from mgraph_db.query.actions.MGraph__Query__Add             import MGraph__Query__Add
from mgraph_db.query.domain.Domain__MGraph__Query           import Domain__MGraph__Query

class test_MGraph__Query__Add(TestCase):

    def setUp(self):
        self.model_graph  = Model__MGraph__Graph ()
        self.graph        = Domain__MGraph__Graph(model = self.model_graph)
        self.mgraph       = MGraph               (graph = self.graph      )
        self.query        = Domain__MGraph__Query(mgraph_data  = self.mgraph.data() ,
                                                  mgraph_index = self.mgraph.index(), )
        self.query.setup()
        self.add_action   = MGraph__Query__Add   (query = self.query)


    # def tearDown(self):
    #     load_dotenv()
    #     mgraph_query = MGraph__Query()
    #     mgraph_query.query_views  = self.query.query_views
    #     mgraph_query.mgraph_index = self.query.mgraph_index
    #     mgraph_query.mgraph_data  = self.query.mgraph_data
    #
    #     with MGraph__Query__Screenshot(mgraph_query=mgraph_query) as _:
    #         _.show_source_graph = True
    #         _.show_node__value  = True
    #         _.save_to('./test_MGraph__Query__Add.both.png')
    #
    #     with self.mgraph.screenshot() as _:
    #         _.load_dotenv   ()
    #         _.show_edge__ids()
    #         _.save_to('test_test_MGraph__Query__Add.png').dot()

    # self.mgraph.edit().create_edge()

    def test_setup(self):
        with self.add_action as _:
            assert type(_) is MGraph__Query__Add
            assert _.query == self.query

    def test_add_node_id(self):                                                     # Test adding single node
        add_action                   = self.add_action
        node                         = self.mgraph.edit().new_node()                                  # Create test node
        result                       = add_action.add_node_id(node.node_id)                           # Add node to view
        current_nodes, current_edges = self.query.get_current_ids()

        assert type(result)     is MGraph__Query__Add
        assert result           == add_action                                                 # Verify result,  Should return self for chaining
        assert current_nodes    == {node.node_id}
        assert current_edges    == set()  # No edges added

        invalid_result               = add_action.add_node_id('invalid_id')         # Test adding non-existent node
        current_nodes, current_edges = self.query.get_current_ids()

        assert invalid_result   == add_action  # Should return self
        assert current_nodes    == {node.node_id}                                     # No change to nodes
        assert current_edges    == set()

    def test_add_nodes_ids(self):                                               # Test adding multiple nodes
        add_action = self.add_action

        # Create test nodes
        node_1 = self.graph.new_node()
        node_2 = self.graph.new_node()
        node_3 = self.graph.new_node()

        # Add multiple nodes
        result = add_action.add_nodes_ids({node_1.node_id, node_2.node_id})

        # Verify initial add
        assert result == add_action
        current_nodes, current_edges = self.query.get_current_ids()
        assert current_nodes == {node_1.node_id, node_2.node_id}
        assert current_edges == set()

        # Add another node
        add_action.add_nodes_ids({node_3.node_id})
        current_nodes, _ = self.query.get_current_ids()
        assert current_nodes == {node_1.node_id, node_2.node_id, node_3.node_id}

        # Test adding mix of valid and invalid nodes
        add_action.add_nodes_ids({node_1.node_id, 'invalid_id'})
        current_nodes, _ = self.query.get_current_ids()
        assert current_nodes == {node_1.node_id, node_2.node_id, node_3.node_id}

        # Test adding only invalid nodes
        add_action.add_nodes_ids({'invalid_1', 'invalid_2'})
        current_nodes, _ = self.query.get_current_ids()
        assert current_nodes == {node_1.node_id, node_2.node_id, node_3.node_id}

    def test_add_node_with_value(self):                                                                 # Test adding node by value
        add_action = self.add_action

        value_node                      = self.graph.new_node(node_type=Schema__MGraph__Node__Value)    # Create value node
        value_node.node_data.value      = "test_value"
        value_node.node_data.value_type = str
        self.query.mgraph_index.values_index.add_value_node(value_node)                                 # Add value to index

        result = add_action.add_node_with_value("test_value")                                           # Test adding by value

        assert result == add_action                                                                     # Verify result
        current_nodes, _ = self.query.get_current_ids()
        assert value_node.node_id in current_nodes

        add_action.add_node_with_value("non_existent_value")                                            # Test adding non-existent value
        current_nodes, _ = self.query.get_current_ids()
        assert current_nodes == {value_node.node_id}                                                    # No change to nodes

    def test_add_outgoing_edges(self):                                          # Test adding outgoing edges
        add_action = self.add_action


        with self.mgraph.edit() as _:                                           # Create test nodes and edges
            node_1 = _.new_node()
            node_2 = _.new_node()
            node_3 = _.new_node()

            edge_1 = _.new_edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
            edge_2 = _.new_edge(from_node_id=node_2.node_id, to_node_id=node_3.node_id)


        result_1                     = add_action.add_node_id(node_1.node_id)               # Start with node_1
        result_2                     = add_action.add_outgoing_edges(depth=1)               # Add outgoing edges with depth=1
        current_nodes, current_edges = self.query.get_current_ids()

        assert result_1      == result_2
        assert result_2      == add_action                                                  # Verify first level
        assert current_nodes == {node_1.node_id, node_2.node_id}
        assert current_edges == {edge_1.edge_id}


        add_action.add_outgoing_edges(depth=2)                                              # Add outgoing edges with depth=2
        current_nodes, current_edges = self.query.get_current_ids()

        assert current_nodes == {node_1.node_id, node_2.node_id, node_3.node_id}
        assert current_edges == {edge_1.edge_id, edge_2.edge_id}

        add_action.add_outgoing_edges(depth=0)                                              # Test with invalid depth
        current_nodes, current_edges = self.query.get_current_ids()
        assert current_nodes == {node_1.node_id, node_2.node_id, node_3.node_id}
        assert current_edges == {edge_1.edge_id, edge_2.edge_id}                            # no changes in current_nodes


        add_action.add_outgoing_edges()                                                     # Test with None depth (should have no impact too)
        current_nodes, current_edges = self.query.get_current_ids()
        assert current_nodes == {node_1.node_id, node_2.node_id, node_3.node_id}
        assert current_edges == {edge_1.edge_id, edge_2.edge_id}


    def test_add_operations_chaining(self):                                                     # Test method chaining
        with self.mgraph.edit() as _:                                                           # Create test data
            node_1 = _.new_node()
            node_2 = _.new_node()
            node_3 = _.new_node()
            edge   = _.connect_nodes(node_1, node_2)

        with self.add_action as _:                                                              # Test chaining multiple operations
            result = (_.add_node_id       (node_1.node_id)
                       .add_nodes_ids     ({node_2.node_id, node_3.node_id})
                       .add_outgoing_edges())

        current_nodes, current_edges = self.query.get_current_ids()                             # Verify final state
        assert result        == self.add_action
        assert current_nodes == {node_1.node_id, node_2.node_id, node_3.node_id}
        assert current_edges == {edge.edge_id}