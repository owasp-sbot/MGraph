# from typing                                          import Type, Callable, Any
# from mgraph_db.mgraph.domain.Domain__MGraph__Node    import Domain__MGraph__Node
# from mgraph_db.mgraph.schemas.Schema__MGraph__Node   import Schema__MGraph__Node
# from mgraph_db.query.domain.Domain__MGraph__Query    import Domain__MGraph__Query
# from osbot_utils.type_safe.Type_Safe                 import Type_Safe
#
#
# class MGraph__Query__Filter(Type_Safe):
#     query: Domain__MGraph__Query                                                   # Reference to domain query
#
#     def by_type(self, node_type: Type[Schema__MGraph__Node]) -> 'MGraph__Query__Filter':
#         matching_ids = self.query.mgraph_index.get_nodes_by_type(node_type)
#         current_nodes, current_edges = self.query.get_current_ids()
#
#         filtered_nodes = matching_ids & current_nodes if current_nodes else matching_ids
#         filtered_edges = self.query.get_connecting_edges(filtered_nodes)
#
#         self.query.create_view(nodes_ids = filtered_nodes,
#                               edges_ids = filtered_edges,
#                               operation = 'by_type',
#                               params    = {'type': node_type.__name__})
#         return self
#
#     def by_predicate(self,
#                      predicate: Callable[[Domain__MGraph__Node], bool]
#                     ) -> 'MGraph__Query__Filter':
#         current_nodes, _ = self.query.get_current_ids()
#         filtered_nodes = {
#             node_id for node_id in current_nodes
#             if predicate(self.query.mgraph_data.node(node_id))
#         }
#
#         filtered_edges = self.query.get_connecting_edges(filtered_nodes)
#
#         self.query.create_view(nodes_ids = filtered_nodes,
#                               edges_ids = filtered_edges,
#                               operation = 'by_predicate',
#                               params    = {'predicate': str(predicate)})
#         return self
#
#     def by_value(self, value: Any) -> 'MGraph__Query__Filter':
#         matching_id = self.query.mgraph_index.get_node_id_by_value(type(value),
#                                                                   str(value))
#         filtered_nodes = {matching_id} if matching_id else set()
#         filtered_edges = self.query.get_connecting_edges(filtered_nodes)
#
#         self.query.create_view(nodes_ids = filtered_nodes,
#                               edges_ids = filtered_edges,
#                               operation = 'by_value',
#                               params    = {'value_type': type(value).__name__,
#                                           'value': str(value)})
#         return self