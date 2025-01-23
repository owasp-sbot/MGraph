from typing                                         import Type, Set, Any
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node  import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge  import Schema__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph import Schema__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Index import Schema__MGraph__Index, Schema__MGraph__Index__Data
from osbot_utils.helpers.Random_Guid                import Random_Guid
from osbot_utils.type_safe.Type_Safe                import Type_Safe
from osbot_utils.utils.Json                         import json_loads, json_dumps


class MGraph__Index(Type_Safe):
    graph : Schema__MGraph__Graph
    index : Schema__MGraph__Index

    def add_node(self, node: Schema__MGraph__Node) -> None:                         # Add a node to the index
        node_id   = node.node_id
        node_type = node.node_type.__name__


        if node_id not in self.index.data.nodes_to_outgoing_edges:                  # Initialize sets if needed
            self.index.data.nodes_to_outgoing_edges[node_id] = set()
        if node_id not in self.index.data.nodes_to_incoming_edges:
            self.index.data.nodes_to_incoming_edges[node_id] = set()


        if node_type not in self.index.data.nodes_by_type:                          # Add to type index
            self.index.data.nodes_by_type[node_type] = set()
        self.index.data.nodes_by_type[node_type].add(node_id)

        # Index attributes
        if hasattr(node, 'attributes') and node.attributes:
            for attr_name, attr_value in node.attributes.items():
                if attr_name not in self.index.data.nodes_by_attribute:
                    self.index.data.nodes_by_attribute[attr_name] = {}
                if attr_value not in self.index.data.nodes_by_attribute[attr_name]:
                    self.index.data.nodes_by_attribute[attr_name][attr_value] = set()
                self.index.data.nodes_by_attribute[attr_name][attr_value].add(node_id)

    def add_edge(self, edge: Schema__MGraph__Edge) -> None:
        """Add an edge to the index"""
        edge_id      = edge.edge_config.edge_id
        from_node_id = edge.from_node_id
        to_node_id   = edge.to_node_id
        edge_type    = edge.edge_type.__name__

        # Add to node relationship indexes
        self.index.data.nodes_to_outgoing_edges[from_node_id].add(edge_id)
        self.index.data.nodes_to_incoming_edges[to_node_id].add(edge_id)
        self.index.data.edge_to_nodes[edge_id] = (from_node_id, to_node_id)

        # Add to type index
        if edge_type not in self.index.data.edges_by_type:
            self.index.data.edges_by_type[edge_type] = set()
        self.index.data.edges_by_type[edge_type].add(edge_id)

        # Index attributes
        if hasattr(edge, 'attributes') and edge.attributes:
            for attr_name, attr_value in edge.attributes.items():
                if attr_name not in self.index.data.edges_by_attribute:
                    self.index.data.edges_by_attribute[attr_name] = {}
                if attr_value not in self.index.data.edges_by_attribute[attr_name]:
                    self.index.data.edges_by_attribute[attr_name][attr_value] = set()
                self.index.data.edges_by_attribute[attr_name][attr_value].add(edge_id)

    def remove_node(self, node: Schema__MGraph__Node) -> None:
        """Remove a node and all its references from the index"""
        node_id = node.node_id

        # Get associated edges before removing node references
        outgoing_edges = self.index.data.nodes_to_outgoing_edges.pop(node_id, set())
        incoming_edges = self.index.data.nodes_to_incoming_edges.pop(node_id, set())

        # Remove from type index
        node_type = node.node_type.__name__
        if node_type in self.index.data.nodes_by_type:
            self.index.data.nodes_by_type[node_type].discard(node_id)
            if not self.index.data.nodes_by_type[node_type]:
                del self.index.data.nodes_by_type[node_type]

        # Remove from attribute indexes
        if hasattr(node, 'attributes') and node.attributes:
            for attr_name, attr_value in node.attributes.items():
                if attr_name in self.index.data.nodes_by_attribute:
                    if attr_value in self.index.data.nodes_by_attribute[attr_name]:
                        self.index.data.nodes_by_attribute[attr_name][attr_value].discard(node_id)

    def remove_edge(self, edge: Schema__MGraph__Edge) -> None:
        """Remove an edge and all its references from the index"""
        edge_id = edge.edge_config.edge_id

        if edge_id in self.index.data.edge_to_nodes:
            from_node_id, to_node_id = self.index.data.edge_to_nodes.pop(edge_id)
            self.index.data.nodes_to_outgoing_edges[from_node_id].discard(edge_id)
            self.index.data.nodes_to_incoming_edges[to_node_id].discard(edge_id)

        # Remove from type index
        edge_type = edge.edge_type.__name__
        if edge_type in self.index.data.edges_by_type:
            self.index.data.edges_by_type[edge_type].discard(edge_id)
            if not self.index.data.edges_by_type[edge_type]:
                del self.index.data.edges_by_type[edge_type]

        # Remove from attribute indexes
        if hasattr(edge, 'attributes') and edge.attributes:
            for attr_name, attr_value in edge.attributes.items():
                if attr_name in self.index.data.edges_by_attribute:
                    if attr_value in self.index.data.edges_by_attribute[attr_name]:
                        self.index.data.edges_by_attribute[attr_name][attr_value].discard(edge_id)

    def get_node_outgoing_edges(self, node: Schema__MGraph__Node) -> Set[Random_Guid]:
        """Get all outgoing edges for a node"""
        return self.index.data.nodes_to_outgoing_edges.get(node.node_id, set())

    def get_node_incoming_edges(self, node: Schema__MGraph__Node) -> Set[Random_Guid]:
        """Get all incoming edges for a node"""
        return self.index.data.nodes_to_incoming_edges.get(node.node_id, set())

    def get_nodes_by_type(self, node_type: Type[Schema__MGraph__Node]) -> Set[Random_Guid]:
        """Get all nodes of a specific type"""
        return self.index.data.nodes_by_type.get(node_type.__name__, set())

    def get_edges_by_type(self, edge_type: Type[Schema__MGraph__Edge]) -> Set[Random_Guid]:
        """Get all edges of a specific type"""
        return self.index.data.edges_by_type.get(edge_type.__name__, set())

    def get_nodes_by_attribute(self, attr_name: str, attr_value: Any) -> Set[Random_Guid]:
        """Get all nodes with a specific attribute value"""
        return self.index.data.nodes_by_attribute.get(attr_name, {}).get(attr_value, set())

    def get_edges_by_attribute(self, attr_name: str, attr_value: Any) -> Set[Random_Guid]:
        """Get all edges with a specific attribute value"""
        return self.index.data.edges_by_attribute.get(attr_name, {}).get(attr_value, set())

    def save_to_file(self, filename: str) -> None:
        """Save the index to a file"""
        # Convert sets to lists for JSON serialization
        data = {
            'nodes_to_outgoing_edges' : {k: list(v) for k, v in self.index.data.nodes_to_outgoing_edges.items()},
            'nodes_to_incoming_edges' : {k: list(v) for k, v in self.index.data.nodes_to_incoming_edges.items()},
            'edge_to_nodes'           : self.index.data.edge_to_nodes,
            'nodes_by_type'           : {k: list(v) for k, v in self.index.data.nodes_by_type.items()},
            'edges_by_type'           : {k: list(v) for k, v in self.index.data.edges_by_type.items()},
            'nodes_by_attribute'      : {k: {attr: list(nodes) for attr, nodes in v.items()}
                                         for k, v in self.index.data.nodes_by_attribute.items()},
            'edges_by_attribute'      : {k: {attr: list(edges) for attr, edges in v.items()}
                                         for k, v in self.index.data.edges_by_attribute.items()}
        }

        with open(filename, 'w') as f:
            f.write(json_dumps(data))

    @classmethod
    def load_from_file(cls, graph: Schema__MGraph__Graph, filename: str) -> 'MGraph__Index':
        """Load the index from a file"""
        with open(filename, 'r') as f:
            json_data = json_loads(f.read())

        # Convert lists back to sets
        data = Schema__MGraph__Index__Data(
            nodes_to_outgoing_edges = {k: set(v) for k, v in json_data['nodes_to_outgoing_edges'].items()},
            nodes_to_incoming_edges = {k: set(v) for k, v in json_data['nodes_to_incoming_edges'].items()},
            edge_to_nodes           = json_data['edge_to_nodes'],
            nodes_by_type           = {k: set(v) for k, v in json_data['nodes_by_type'].items()},
            edges_by_type           = {k: set(v) for k, v in json_data['edges_by_type'].items()},
            nodes_by_attribute      = {k: {attr: set(nodes) for attr, nodes in v.items()}
                                       for k, v in json_data['nodes_by_attribute'].items()},
            edges_by_attribute      = {k: {attr: set(edges) for attr, edges in v.items()}
                                       for k, v in json_data['edges_by_attribute'].items()}
        )

        return cls(graph=graph, index=Schema__MGraph__Index(data=data))