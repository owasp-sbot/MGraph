# from unittest                                               import TestCase
#
# import pytest
#
# from mgraph_db.mgraph.MGraph                                import MGraph
# from mgraph_db.mgraph.domain.Domain__MGraph__Graph          import Domain__MGraph__Graph
# from mgraph_db.mgraph.domain.Domain__MGraph__Node           import Domain__MGraph__Node
# from mgraph_db.mgraph.models.Model__MGraph__Graph           import Model__MGraph__Graph
# from mgraph_db.mgraph.schemas.Schema__MGraph__Node          import Schema__MGraph__Node
# from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value   import Schema__MGraph__Node__Value
# from mgraph_db.query.MGraph__Query                          import MGraph__Query
# from mgraph_db.query.actions.MGraph__Query__Filter          import MGraph__Query__Filter
# from mgraph_db.query.actions.MGraph__Query__Screenshot      import MGraph__Query__Screenshot
# from mgraph_db.query.domain.Domain__MGraph__Query           import Domain__MGraph__Query
# from osbot_utils.utils.Env                                  import load_dotenv
#
#
# class Custom_Node(Schema__MGraph__Node): pass                               # Create custom node type for testing
#
# class test_MGraph__Query__Filter(TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         pytest.skip("Needs fixing after refactoring of MGraph__Index")  # todo: for example get_nodes_by_field() doesn't exist any more
#
#     def setUp(self):
#         self.model_graph   = Model__MGraph__Graph ()
#         self.graph         = Domain__MGraph__Graph(model = self.model_graph)
#         self.mgraph        = MGraph               (graph = self.graph      )
#         self.query         = Domain__MGraph__Query(mgraph_data  = self.mgraph.data() ,
#                                                   mgraph_index = self.mgraph.index())
#         self.query.setup()
#         self.filter_action = MGraph__Query__Filter(query = self.query)
#
#     def tearDown(self):
#         load_dotenv()
#         mgraph_query = MGraph__Query()
#         mgraph_query.query_views  = self.query.query_views
#         mgraph_query.mgraph_index = self.query.mgraph_index
#         mgraph_query.mgraph_data  = self.query.mgraph_data
#
#         with MGraph__Query__Screenshot(mgraph_query=mgraph_query) as _:
#             #_.show_source_graph = True
#             #_.show_node__value  = True
#             #_.show_node__type  = True
#             _.save_to('./test_MGraph__Query__Filter.both.png')
#
#         # with self.mgraph.screenshot() as _:
#         #     _.load_dotenv   ()
#         #     _.show_edge__id()
#         #     _.save_to('test_MGraph__Query__Filter.png').dot()
#
#     #self.mgraph.edit().create_edge()
#
#     def test_setup(self):
#         with self.filter_action as _:
#             assert type(_) is MGraph__Query__Filter
#             assert _.query == self.query
#
#     def test_by_type(self):                                                         # Test filtering by node type
#         filter_action = self.filter_action
#
#         with self.mgraph.edit() as _:                                              # Create test nodes of different types
#             node_1 = _.new_node(node_type=Schema__MGraph__Node)
#             node_2 = _.new_node(node_type=Custom_Node         )
#             node_3 = _.new_node(node_type=Custom_Node         )
#             _.connect_nodes(node_1, node_2)                                         # Add some edges
#             _.connect_nodes(node_2, node_3)
#
#         result = filter_action.by_type(Custom_Node)                                 # Filter by custom node type
#
#         current_nodes, current_edges = self.query.get_current_ids()                 # Verify results
#         assert result == filter_action                                              # Should return self for chaining
#         assert current_nodes == {node_2.node_id, node_3.node_id}                    # Should only include Custom_Node nodes
#         assert len(current_edges) > 0                                               # Should include connecting edges
#
#     def test_by_predicate(self):                                                   # Test filtering by predicate
#         filter_action = self.filter_action
#
#         with self.mgraph.edit() as _:                                              # Create test nodes
#             node_1 = _.new_node(node_type=Schema__MGraph__Node__Value)             # Set up nodes with different values
#             node_2 = _.new_node(node_type=Schema__MGraph__Node__Value)
#             node_3 = _.new_node(node_type=Schema__MGraph__Node__Value)
#
#             node_1.node_data.value = "test_1"                                       # Set values
#             node_2.node_data.value = "test_2"
#             node_3.node_data.value = "other"
#
#             edge_1 = _.connect_nodes(node_1, node_2)                               # Add connections
#             edge_2 = _.connect_nodes(node_2, node_3)
#
#         def predicate(node: Domain__MGraph__Node) -> bool:                         # Define test predicate
#             return node.node_data and hasattr(node.node_data, 'value') and 'test' in str(node.node_data.value)
#
#         result = filter_action.by_predicate(predicate)                             # Apply filter
#
#         current_nodes, current_edges = self.query.get_current_ids()                 # Verify results
#         assert result == filter_action
#         assert current_nodes == {node_1.node_id, node_2.node_id}                   # Only nodes with 'test' in value
#         assert edge_1.edge_id in current_edges                                     # Edge between matching nodes
#         assert edge_2.edge_id not in current_edges                                 # Edge to non-matching node excluded
#
#     def test_by_value(self):                                                       # Test filtering by exact value
#         filter_action = self.filter_action
#
#         with self.mgraph.edit() as _:                                              # Create test nodes with values
#             node_1 = _.new_node(node_type=Schema__MGraph__Node__Value)
#             node_2 = _.new_node(node_type=Schema__MGraph__Node__Value)
#
#             node_1.node_data.value = "test_value"                                   # Set values
#             node_1.node_data.value_type = str
#             node_2.node_data.value = "other_value"
#             node_2.node_data.value_type = str
#
#             self.query.mgraph_index.values_index.add_value_node(node_1)            # Add values to index
#             self.query.mgraph_index.values_index.add_value_node(node_2)
#
#             edge = _.connect_nodes(node_1, node_2)                                 # Add connection
#
#         result = filter_action.by_value("test_value")                              # Filter by value
#
#         current_nodes, current_edges = self.query.get_current_ids()                 # Verify results
#         assert result == filter_action
#         assert current_nodes == {node_1.node_id}                                   # Only node with matching value
#         assert current_edges == set()                                              # No edges since no connecting filtered nodes
#
#         filter_action.by_value("non_existent_value")                               # Test with non-existent value
#         current_nodes, current_edges = self.query.get_current_ids()
#         assert current_nodes == set()                                              # No nodes should match
#         assert current_edges == set()                                              # No edges
#
#     def test_filter_operations_chaining(self):                                     # Test method chaining
#         filter_action = self.filter_action
#
#         class Custom_Node(Schema__MGraph__Node): pass                               # Create custom node type
#
#         with self.mgraph.edit() as _:                                              # Create test data
#             node_1 = _.new_node(node_type=Custom_Node)                             # Custom type nodes
#             node_2 = _.new_node(node_type=Custom_Node)
#             node_3 = _.new_node(node_type=Schema__MGraph__Node__Value)             # Value node
#
#             node_3.node_data.value = "test_value"                                   # Set up value node
#             node_3.node_data.value_type = str
#             self.query.mgraph_index.values_index.add_value_node(node_3)
#
#             _.connect_nodes(node_1, node_2)                                         # Add connections
#             _.connect_nodes(node_2, node_3)
#
#         def custom_predicate(node: Domain__MGraph__Node) -> bool:                  # Define test predicate
#             return isinstance(node.node.data, Custom_Node)
#
#         result = (filter_action                                                     # Chain multiple filters
#                  .by_type(Custom_Node)
#                  .by_predicate(custom_predicate))
#
#         current_nodes, current_edges = self.query.get_current_ids()                 # Verify final state
#         assert result == filter_action
#         assert len(current_nodes) == 2                                             # Should have both Custom_Node nodes
#         assert len(current_edges) == 1                                             # Should have the edge between them