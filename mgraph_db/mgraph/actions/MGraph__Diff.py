from dataclasses                                    import dataclass
from typing                                         import Dict, Set, Any
from mgraph_db.mgraph.domain.Domain__MGraph__Graph  import Domain__MGraph__Graph
from mgraph_db.mgraph.domain.Domain__MGraph__Node   import Domain__MGraph__Node
from mgraph_db.mgraph.domain.Domain__MGraph__Edge   import Domain__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Diff  import Schema__MGraph__Diff
from osbot_utils.helpers.Obj_Id                     import Obj_Id
from osbot_utils.type_safe.Type_Safe                import Type_Safe




class MGraph__Diff(Type_Safe):
    graph_a: Domain__MGraph__Graph
    graph_b: Domain__MGraph__Graph

    def diff_graphs(self) -> Schema__MGraph__Diff:           #Compare two graphs and return detailed statistics about their differences"""

        nodes_a = set(self.graph_a.nodes_ids())         # Get sets of node and edge IDs from both graphs
        nodes_b = set(self.graph_b.nodes_ids())
        edges_a = set(self.graph_a.edges_ids())
        edges_b = set(self.graph_b.edges_ids())

        nodes_added   = nodes_b - nodes_a               # Find added and removed nodes
        nodes_removed = nodes_a - nodes_b


        nodes_modified = set()                          # Find modified nodes (same ID but different data)
        nodes_common   = nodes_a & nodes_b
        for node_id in nodes_common:
            node_a = self.graph_a.node(node_id)
            node_b = self.graph_b.node(node_id)
            if not self.nodes_equal(node_a, node_b):
                nodes_modified.add(node_id)

        edges_added   = edges_b - edges_a               # Find added and removed edges
        edges_removed = edges_a - edges_b


        edges_modified = set()                          # Find modified edges (same ID but different data)
        edges_common  = edges_a & edges_b
        for edge_id in edges_common:
            edge_a = self.graph_a.edge(edge_id)
            edge_b = self.graph_b.edge(edge_id)
            if not self.edges_equal(edge_a, edge_b):
                edges_modified.add(edge_id)

        return Schema__MGraph__Diff(nodes_added      = sorted(nodes_added),
                                    nodes_removed    = sorted(nodes_removed      ),
                                    nodes_modified   = sorted(nodes_modified     ),
                                    edges_added      = sorted(edges_added        ),
                                    edges_removed    = sorted(edges_removed      ),
                                    edges_modified   = sorted(edges_modified     ),
                                    nodes_count_diff = len(nodes_b) - len(nodes_a),
                                    edges_count_diff = len(edges_b) - len(edges_a))

    def compare_node_data(self, node_id: Obj_Id) -> Dict[str, Any]:                     # Compare data for a specific node between the two graphs
        node_a = self.graph_a.node(node_id)
        node_b = self.graph_b.node(node_id)

        if not node_a or not node_b:
            return {}

        changes = {}
        if node_a.node_data != node_b.node_data:
            changes['data'] = { 'from': node_a.node_data.json() if node_a.node_data else None ,
                                'to'  : node_b.node_data.json() if node_b.node_data else None }

        if node_a.node_type != node_b.node_type:
            changes['type'] = { 'from': node_a.node_type.__name__,
                                'to'  : node_b.node_type.__name__ }

        return changes

    def compare_edge_data(self, edge_id: Obj_Id) -> Dict[str, Any]:                     # Compare data for a specific edge between the two graphs"""
        edge_a = self.graph_a.edge(edge_id)
        edge_b = self.graph_b.edge(edge_id)

        if not edge_a or not edge_b:
            return {}

        changes = {}
        if edge_a.edge.data.edge_type != edge_b.edge.data.edge_type:
            changes['type'] = {
                'from': edge_a.edge.data.edge_type.__name__,
                'to': edge_b.edge.data.edge_type.__name__
            }

        if edge_a.from_node_id() != edge_b.from_node_id():
            changes['from_node'] = {
                'from': str(edge_a.from_node_id()),
                'to': str(edge_b.from_node_id())
            }

        if edge_a.to_node_id() != edge_b.to_node_id():
            changes['to_node'] = {
                'from': str(edge_a.to_node_id()),
                'to': str(edge_b.to_node_id())
            }

        return changes

    def nodes_equal(self, node_a: Domain__MGraph__Node, node_b: Domain__MGraph__Node) -> bool:                         # Compare two nodes for equality
        if not node_a or not node_b:
            return False

        return (node_a.node_type == node_b.node_type and
                node_a.node_data == node_b.node_data)

    def edges_equal(self, edge_a: Domain__MGraph__Edge, edge_b: Domain__MGraph__Edge) -> bool:                          # Compare two edges for equality
        if not edge_a or not edge_b:
            return False

        return (edge_a.edge.data.edge_type == edge_b.edge.data.edge_type and
                edge_a.from_node_id() == edge_b.from_node_id() and
                edge_a.to_node_id() == edge_b.to_node_id())