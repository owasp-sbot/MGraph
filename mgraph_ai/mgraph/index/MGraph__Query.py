from typing                                 import Any, Dict, List, Optional, Set, Type, Union, Iterable
from mgraph_ai.mgraph.actions.MGraph__Data  import MGraph__Data
from mgraph_ai.mgraph.index.MGraph__Index   import MGraph__Index
from osbot_utils.helpers.Obj_Id             import Obj_Id
from osbot_utils.type_safe.Type_Safe        import Type_Safe

class MGraph__Query(Type_Safe):
    mgraph_index        : MGraph__Index
    mgraph_data         : MGraph__Data
    current_node_ids    : Set[Obj_Id]
    current_node_type   : Optional[str]
    current__filters    : List[Dict[str, Any]]

    def _get_property(self, name: str) -> 'MGraph__Query':
        if not self.current_node_ids:
            return self._empty_query()

        result_nodes = set()
        for node_id in self.current_node_ids:
            outgoing_edges = self.mgraph_index.get_node_outgoing_edges(self.mgraph_data.node(node_id))
            for edge_id in outgoing_edges:
                edge        = self.mgraph_data.edge(edge_id)
                target_node = self.mgraph_data.node(edge.to_node_id)
                if hasattr(target_node.node_data, 'name') and target_node.node_data.name == name:         # todo: remove hard code
                    result_nodes.add(edge.to_node_id)

        new_query = MGraph__Query(index=self.mgraph_index, graph=self.mgraph_data)
        new_query.current_node_ids = result_nodes
        if result_nodes:
            new_query.current_node_type = self.mgraph_data.node(next(iter(result_nodes))).node_type.__name__
        return new_query

    def _empty_query(self) -> 'MGraph__Query':
        return MGraph__Query(mgraph_index=self.mgraph_index, mgraph_data=self.mgraph_data)

    def by_type(self, node_type: Type) -> 'MGraph__Query':
        matching_nodes = self.mgraph_index.get_nodes_by_type(node_type)
        if not matching_nodes:
            return self._empty_query()

        new_query = MGraph__Query(mgraph_index=self.mgraph_index, mgraph_data=self.mgraph_data)
        new_query.current_node_ids = matching_nodes
        new_query.current_node_type = node_type.__name__
        return new_query

    def with_field(self, name: str, value: Any) -> 'MGraph__Query':
        matching_nodes = self.mgraph_index.get_nodes_by_field(name, value)
        if not matching_nodes:
            return self._empty_query()

        new_query = MGraph__Query(mgraph_index=self.mgraph_index, mgraph_data=self.mgraph_data)
        first_node_id  = next(iter(matching_nodes))
        first_node                   =self.mgraph_data.node(first_node_id)
        node_type_name              = first_node.node.node_type.__name__
        new_query.current_node_ids  = matching_nodes
        new_query.current_node_type = node_type_name
        return new_query

    def traverse(self, edge_type: Optional[Type] = None) -> 'MGraph__Query':
        if not self.current_node_ids:
            return self._empty_query()

        result_nodes = set()
        for node_id in self.current_node_ids:
            outgoing_edges = self.mgraph_index.get_node_outgoing_edges(self.mgraph_data.node(node_id))
            if edge_type:
                outgoing_edges = {edge_id for edge_id in outgoing_edges
                                  if self.mgraph_data.edge(edge_id).edge.data.edge_type == edge_type}

            for edge_id in outgoing_edges:
                edge = self.mgraph_data.edge(edge_id)
                result_nodes.add(edge.to_node_id)

        new_query = MGraph__Query(mgraph_index=self.mgraph_index, mgraph_data=self.mgraph_data)
        new_query.current_node_ids = result_nodes
        if result_nodes:
            next_node_id = next(iter(result_nodes))
            current_node = self.mgraph_data.node(next_node_id)
            if current_node:
                new_query.current_node_type = current_node.node_type.__name__
        return new_query

    def filter(self, predicate: callable) -> 'MGraph__Query':
        if not self.current_node_ids:
            return self._empty_query()

        matching_nodes = {node_id for node_id in self.current_node_ids
                          if predicate(self.mgraph_data.node(node_id))}

        new_query = MGraph__Query(mgraph_index=self.mgraph_index, mgraph_data=self.mgraph_data)
        new_query.current_node_ids = matching_nodes
        if matching_nodes:
            current_node= self.mgraph_data.node(next(iter(matching_nodes)))
            if current_node:
                new_query.current_node_type = current_node.node.node_type.__name__
        return new_query

    def collect(self) -> List[Any]:
        if not self.current_node_ids:
            return []

        results = []
        for node_id in self.current_node_ids:
            node = self.mgraph_data.node(node_id)
            if hasattr(node, 'value'):
                results.append(node.value)
            elif hasattr(node, 'name'):
                results.append(node.name)
            else:
                results.append(node)
        return results

    def value(self) -> Any:
        if not self.current_node_ids:
            return None

        values = []
        for node_id in self.current_node_ids:
            node = self.mgraph_data.node(node_id)
            if hasattr(node, 'value'):
                values.append(node.value)

        return values[0] if values else None

    def count(self) -> int:
        return len(self.current_node_ids)

    def exists(self) -> bool:
        return bool(self.current_node_ids)

    def first(self) -> Optional[Any]:
        if not self.current_node_ids:
            return None
        node_id = next(iter(self.current_node_ids))
        return self.mgraph_data.node(node_id)

    def __bool__(self) -> bool:
        return bool(self.current_node_ids)