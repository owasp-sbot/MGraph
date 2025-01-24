from typing                               import Any, Dict, List, Optional, Set, Type, Union
from mgraph_ai.mgraph.index.MGraph__Index import MGraph__Index
from osbot_utils.helpers.Random_Guid      import Random_Guid
from osbot_utils.type_safe.Type_Safe      import Type_Safe


class Graph__Query(Type_Safe):
    index       : MGraph__Index
    graph       : Any

    _current_node_id    : Optional[Random_Guid] = None
    _current_node_type  : Optional[str        ] = None
    _filters            : List[Dict[str, Any]  ] = []

    def _get_property(self, name: str) -> 'Graph__Query':                        # Navigate through a property edge
        if not self._current_node_id:
            return self._empty_query()

        outgoing_edges = self.index.get_node_outgoing_edges(self._current_node_id)
        for edge_id in outgoing_edges:
            edge        = self.graph.edges[edge_id]
            target_node = self.graph.nodes[edge.to_node_id]
            if hasattr(target_node, 'name') and target_node.name == name:
                new_query = Graph__Query(self.index)
                new_query._current_node_id   = edge.to_node_id
                new_query._current_node_type = target_node.node_type.__name__
                return new_query

        return self._empty_query()

    def _empty_query(self) -> 'Graph__Query':                                   # Return an empty query instance
        return Graph__Query(self.index)

    def by_type(self, node_type: Type) -> 'Graph__Query':                        # Filter nodes by type
        matching_nodes = self.index.get_nodes_by_type(node_type)
        if not matching_nodes:
            return self._empty_query()

        new_query = Graph__Query(self.index)
        new_query._current_node_id   = list(matching_nodes)[0]                   # Get first match
        new_query._current_node_type = node_type.__name__
        return new_query

    def with_attribute(self, name: str, value: Any) -> 'Graph__Query':            # Filter nodes by attribute value
        matching_nodes = self.index.get_nodes_by_attribute(name, value)
        if not matching_nodes:
            return self._empty_query()

        new_query = Graph__Query(self.index)
        new_query._current_node_id = list(matching_nodes)[0]
        return new_query

    def traverse(self, edge_type: Optional[Type] = None) -> 'Graph__Query':       # Traverse to connected nodes
        if not self._current_node_id:
            return self._empty_query()

        outgoing_edges = self.index.get_node_outgoing_edges(self._current_node_id)
        if edge_type:
            outgoing_edges = {edge_id for edge_id in outgoing_edges
                            if self.graph.edges[edge_id].edge_type == edge_type}

        if not outgoing_edges:
            return self._empty_query()


        edge_id = list(outgoing_edges)[0]                                           # Get first connected node
        edge    = self.graph.edges[edge_id]

        new_query = Graph__Query(self.index)
        new_query._current_node_id   = edge.to_node_id
        new_query._current_node_type = self.graph.nodes[edge.to_node_id].node_type.__name__
        return new_query

    def collect(self) -> List[Any]:                                                 # Collect all matching nodes
        if not self._current_node_id:
            return []

        results = []
        node    = self.graph.nodes[self._current_node_id]

        # Handle value nodes
        if hasattr(node, 'value'):
            results.append(node.value)
        # Handle property nodes
        elif hasattr(node, 'name'):
            results.append(node.name)
        # Handle other node types
        else:
            results.append(node)

        return results

    def value(self) -> Any:                                                      # Get the value of the current node
        if not self._current_node_id:
            return None

        node = self.graph.nodes[self._current_node_id]
        return getattr(node, 'value', None)

    def __getattr__(self, name: str) -> 'Graph__Query':                           # Enable property-based traversal
        return self._get_property(name)

    def __call__(self, *args, **kwargs) -> Any:                                   # Make query callable to get value
        return self.value()

    def __bool__(self) -> bool:                                                   # Enable truthiness check
        return self._current_node_id is not None