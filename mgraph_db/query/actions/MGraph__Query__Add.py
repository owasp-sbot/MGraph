from typing                                         import Set, Optional
from mgraph_db.query.domain.Domain__MGraph__Query    import Domain__MGraph__Query
from osbot_utils.helpers.Obj_Id                      import Obj_Id
from osbot_utils.type_safe.Type_Safe                 import Type_Safe


class MGraph__Query__Add(Type_Safe):
    query: Domain__MGraph__Query                                                    # Reference to domain query

    def add_node_id(self, node_id: Obj_Id) -> 'MGraph__Query__Add':               # Add specific node to view
        current_nodes, current_edges = self.query.get_current_ids()                # Get current state

        if not self.query.mgraph_data.node(node_id):                              # Validate node exists
            return self

        new_nodes = current_nodes | {node_id}                                      # Add new node to set
        new_edges = current_edges                                                  # Keep current edges

        self.query.create_view(nodes_ids = new_nodes,
                              edges_ids = new_edges,
                              operation = 'add_node_id',
                              params    = {'node_id': str(node_id)})              # Create new view with added node
        return self

    def add_nodes_ids(self, nodes_ids: Set[Obj_Id]) -> 'MGraph__Query__Add':     # Add multiple nodes to view
        current_nodes, current_edges = self.query.get_current_ids()               # Get current state

        valid_nodes = {node_id for node_id in nodes_ids                          # Filter valid nodes
                        if self.query.mgraph_data.node(node_id)}

        if not valid_nodes:                                                       # Return if no valid nodes
            return self

        new_nodes = current_nodes | valid_nodes                                   # Add new nodes to set
        new_edges = current_edges                                                 # Keep current edges

        self.query.create_view(nodes_ids = new_nodes,
                              edges_ids = new_edges,
                              operation = 'add_nodes_ids',
                              params    = {'nodes_ids': [str(node_id)
                                                       for node_id in valid_nodes]})
        return self

    def add_node_with_value(self, value: any) -> 'MGraph__Query__Add':          # Add node with specific value
        matching_id = self.query.mgraph_index.get_node_id_by_value(type(value),
                                                                  str(value))
        if matching_id:
            filtered_nodes = {matching_id}                                        # Start with matching node
            filtered_edges = set()

            # Get all incoming edges to build path
            current_node_id = matching_id
            while True:
                incoming_edges = self.query.mgraph_index.edges_ids__to__node_id(current_node_id)
                if not incoming_edges:
                    break

                edge_id = incoming_edges[0]                                      # Take first incoming edge
                edge = self.query.mgraph_data.edge(edge_id)
                filtered_edges.add(edge_id)

                parent_node_id = edge.from_node_id()
                filtered_nodes.add(parent_node_id)

                # Add sibling nodes
                outgoing_edges = self.query.mgraph_index.edges_ids__from__node_id(parent_node_id)
                for sibling_edge_id in outgoing_edges:
                    sibling_edge = self.query.mgraph_data.edge(sibling_edge_id)
                    filtered_edges.add(sibling_edge_id)
                    filtered_nodes.add(sibling_edge.to_node_id())

                current_node_id = parent_node_id                                # Move up to parent

            self.query.create_view(nodes_ids = filtered_nodes,
                                  edges_ids = filtered_edges,
                                  operation = 'add_node_with_value',
                                  params    = {'value_type': type(value).__name__,
                                              'value'     : str(value)})
        return self

    def add_outgoing_edges(self, depth: Optional[int] = None) -> 'MGraph__Query__Add':    # Add outgoing edges
        if depth is not None and depth <= 0:
            return self

        current_nodes, current_edges = self.query.get_current_ids()             # Get current state
        new_nodes = set()                                                       # Initialize new sets
        new_edges = set()

        for node_id in current_nodes:                                          # Process each current node
            node = self.query.mgraph_data.node(node_id)
            if node:
                outgoing_edges = self.query.mgraph_index.get_node_outgoing_edges(node)
                new_edges.update(outgoing_edges)

                for edge_id in outgoing_edges:                                 # Add target nodes
                    edge = self.query.mgraph_data.edge(edge_id)
                    if edge:
                        new_nodes.add(edge.to_node_id())

        combined_nodes = current_nodes | new_nodes                             # Combine sets
        combined_edges = current_edges | new_edges

        self.query.create_view(nodes_ids = combined_nodes,
                              edges_ids = combined_edges,
                              operation = 'add_outgoing_edges',
                              params    = {'depth': depth})

        if depth is not None:                                                 # Recursive case for depth
            return self.add_outgoing_edges(depth - 1)

        return self