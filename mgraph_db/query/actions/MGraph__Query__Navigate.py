# from typing                                          import Type, Optional, Set
# from mgraph_db.mgraph.schemas.Schema__MGraph__Edge   import Schema__MGraph__Edge
# from mgraph_db.query.domain.Domain__MGraph__Query    import Domain__MGraph__Query
# from osbot_utils.type_safe.Type_Safe                 import Type_Safe
#
#
# class MGraph__Query__Navigate(Type_Safe):
#     query: Domain__MGraph__Query                                                   # Reference to domain query
#
#     def to_connected_nodes(self,
#                           edge_type: Optional[Type[Schema__MGraph__Edge]] = None,
#                           direction: str = 'outgoing') -> 'MGraph__Query__Navigate':
#         current_nodes, _ = self.query.get_current_ids()
#         connected_nodes = set()
#         connected_edges = set()
#
#         for node_id in current_nodes:
#             node = self.query.mgraph_data.node(node_id)
#             if node:
#                 # Get edges based on direction
#                 if direction == 'outgoing':
#                     edges = self.query.mgraph_index.get_node_outgoing_edges(node)
#                 elif direction == 'incoming':
#                     edges = self.query.mgraph_index.get_node_incoming_edges(node)
#                 else:
#                     raise ValueError(f"Invalid direction: {direction}")
#
#                 # Filter by edge type if specified
#                 if edge_type:
#                     edges = {edge_id for edge_id in edges
#                             if isinstance(self.query.mgraph_data.edge(edge_id), edge_type)}
#
#                 # Get connected nodes
#                 for edge_id in edges:
#                     edge = self.query.mgraph_data.edge(edge_id)
#                     if edge:
#                         connected_edges.add(edge_id)
#                         if direction == 'outgoing':
#                             connected_nodes.add(edge.to_node_id())
#                         else:
#                             connected_nodes.add(edge.from_node_id())
#
#         self.query.create_view(nodes_ids = connected_nodes,
#                               edges_ids = connected_edges,
#                               operation = 'to_connected_nodes',
#                               params    = {'edge_type': edge_type.__name__ if edge_type else None,
#                                           'direction': direction})
#         return self
#
#     def to_outgoing(self,
#                     edge_type: Optional[Type[Schema__MGraph__Edge]] = None
#                    ) -> 'MGraph__Query__Navigate':
#         return self.to_connected_nodes(edge_type=edge_type, direction='outgoing')
#
#     def to_incoming(self,
#                     edge_type: Optional[Type[Schema__MGraph__Edge]] = None
#                    ) -> 'MGraph__Query__Navigate':
#         return self.to_connected_nodes(edge_type=edge_type, direction='incoming')
#
#     def follow_path(self, edge_types: list[Type[Schema__MGraph__Edge]]) -> 'MGraph__Query__Navigate':
#         for edge_type in edge_types:
#             self.to_outgoing(edge_type)
#         return self
#
#     def to_root(self) -> 'MGraph__Query__Navigate':                              # Navigate to root nodes
#         current_nodes, _ = self.query.get_current_ids()
#         root_nodes = set()
#         edges_to_roots = set()
#
#         for node_id in current_nodes:
#             current_node_id = node_id
#             while True:
#                 incoming_edges = self.query.mgraph_index.edges_ids__to__node_id(current_node_id)
#                 if not incoming_edges:                                           # Found a root node
#                     root_nodes.add(current_node_id)
#                     break
#
#                 edge_id = incoming_edges[0]                                     # Take first incoming edge
#                 edge = self.query.mgraph_data.edge(edge_id)
#                 edges_to_roots.add(edge_id)
#                 current_node_id = edge.from_node_id()
#                 root_nodes.add(current_node_id)
#
#         self.query.create_view(nodes_ids = root_nodes,
#                               edges_ids = edges_to_roots,
#                               operation = 'to_root',
#                               params    = {})
#         return self