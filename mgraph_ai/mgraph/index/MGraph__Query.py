from typing                                 import Any, Dict, List, Optional, Set, Type, Union, Iterable
from mgraph_ai.mgraph.index.MGraph__Index   import MGraph__Index
from osbot_utils.helpers.Obj_Id             import Obj_Id
from osbot_utils.type_safe.Type_Safe        import Type_Safe

class MGraph__Query(Type_Safe):
    index               : MGraph__Index
    graph               : Any                           # Reference to graph for data access

    current_node_ids   : Set[Obj_Id]                   # Support multiple active nodes
    current_node_type  : Optional[str]
    current__filters   : List[Dict[str, Any]]


    def _get_property(self, name: str) -> 'MGraph__Query':
        """Navigate through property edges, preserving type safety"""
        if not self.current_node_ids:
            return self._empty_query()

        result_nodes = set()
        for node_id in self.current_node_ids:
            outgoing_edges = self.index.get_node_outgoing_edges(self.graph.nodes[node_id])
            for edge_id in outgoing_edges:
                edge = self.graph.edges[edge_id]
                target_node = self.graph.nodes[edge.to_node_id]
                if hasattr(target_node, 'name') and target_node.name == name:
                    result_nodes.add(edge.to_node_id)

        new_query = MGraph__Query(self.index, self.graph)
        new_query.current_node_ids = result_nodes
        if result_nodes:
            new_query.current_node_type = self.graph.nodes[next(iter(result_nodes))].node_type.__name__
        return new_query

    def _empty_query(self) -> 'MGraph__Query':
        """Return an empty query instance"""
        return MGraph__Query(index=self.index, graph=self.graph)

    def by_type(self, node_type: Type) -> 'MGraph__Query':                  # Filter nodes by type with O(1) lookup
        matching_nodes = self.index.get_nodes_by_type(node_type)
        if not matching_nodes:
            return self._empty_query()

        new_query = MGraph__Query(index=self.index, graph=self.graph)
        new_query.current_node_ids = matching_nodes
        new_query.current_node_type = node_type.__name__
        return new_query

    def with_attribute(self, name: str, value: Any) -> 'MGraph__Query':
        """Filter nodes by attribute using index"""
        matching_nodes = self.index.get_nodes_by_attribute(name, value)
        if not matching_nodes:
            return self._empty_query()

        new_query = MGraph__Query(self.index, self.graph)
        new_query.current_node_ids = matching_nodes
        if matching_nodes:
            new_query.current_node_type = self.graph.nodes[next(iter(matching_nodes))].node_type.__name__
        return new_query

    def traverse(self, edge_type: Optional[Type] = None) -> 'MGraph__Query':
        """Traverse to connected nodes efficiently"""
        if not self.current_node_ids:
            return self._empty_query()

        result_nodes = set()
        for node_id in self.current_node_ids:
            outgoing_edges = self.index.get_node_outgoing_edges(self.graph.nodes[node_id])
            if edge_type:
                outgoing_edges = {edge_id for edge_id in outgoing_edges
                                if self.graph.edges[edge_id].edge_type == edge_type}

            for edge_id in outgoing_edges:
                edge = self.graph.edges[edge_id]
                result_nodes.add(edge.to_node_id)

        new_query = MGraph__Query(self.index, self.graph)
        new_query.current_node_ids = result_nodes
        if result_nodes:
            new_query.current_node_type = self.graph.nodes[next(iter(result_nodes))].node_type.__name__
        return new_query

    def filter(self, predicate: callable) -> 'MGraph__Query':
        """Apply custom filter to current nodes"""
        if not self.current_node_ids:
            return self._empty_query()

        matching_nodes = {node_id for node_id in self.current_node_ids
                        if predicate(self.graph.nodes[node_id])}

        new_query = MGraph__Query(self.index, self.graph)
        new_query.current_node_ids = matching_nodes
        if matching_nodes:
            new_query.current_node_type = self.graph.nodes[next(iter(matching_nodes))].node_type.__name__
        return new_query

    def collect(self) -> List[Any]:
        """Collect all matching nodes preserving type information"""
        if not self.current_node_ids:
            return []

        results = []
        for node_id in self.current_node_ids:
            node = self.graph.nodes[node_id]
            if hasattr(node, 'value'):
                results.append(node.value)
            elif hasattr(node, 'name'):
                results.append(node.name)
            else:
                results.append(node)
        return results

    def value(self) -> Any:
        """Get value of current node(s)"""
        if not self.current_node_ids:
            return None

        values = []
        for node_id in self.current_node_ids:
            node = self.graph.nodes[node_id]
            if hasattr(node, 'value'):
                values.append(node.value)

        return values[0] if values else None

    def count(self) -> int:                                         #   Count matching nodes
        return len(self.current_node_ids)

    def exists(self) -> bool:
        """Check if any nodes match the query"""
        return bool(self.current_node_ids)

    def first(self) -> Optional[Any]:
        """Get first matching node"""
        if not self.current_node_ids:
            return None
        node_id = next(iter(self.current_node_ids))
        return self.graph.nodes[node_id]

    # def __getattr__(self, name: str) -> 'MGraph__Query':
    #     """Enable property-based traversal"""
    #     return self._get_property(name)

    def __bool__(self) -> bool:
        """Enable truthiness check"""
        return bool(self.current_node_ids)