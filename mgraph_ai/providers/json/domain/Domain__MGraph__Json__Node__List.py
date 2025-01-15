from typing                                                     import List, Any
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node import Domain__MGraph__Json__Node
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node  import Model__MGraph__Json__Node__List, Model__MGraph__Json__Node__Value


class Domain__MGraph__Json__Node__List(Domain__MGraph__Json__Node):
    node: Model__MGraph__Json__Node__List                                                                               # Reference to list node model

    def items(self) -> List[Any]:                                                                                       # Get all items in the list
        items = []
        for edge in self.models__from_edges():
            value_node = self.graph.node(edge.to_node_id())
            if isinstance(value_node, Model__MGraph__Json__Node__Value):
                items.append(value_node.value)
        return items

    def add(self, value: Any) -> None:                                                           # Add an item to the list
        value_node = self.graph.new_node(value=value, value_type=type(value))
        self.graph.new_edge(from_node_id=self.node_id(), to_node_id=value_node.node_id())

    def clear(self) -> None:                                                                    # Remove all items
        for edge in self.models__from_edges():
            self.graph.delete_edge(edge.edge_id())

    def extend(self, nodes: List[Domain__MGraph__Json__Node]) -> None:
        """Add multiple nodes to the list"""
        for node in nodes:
            self.graph.new_edge(from_node_id = self.node_id(),
                                to_node_id   = node.node_id())

    def remove(self, value: Any) -> bool:                                                        # Remove first occurrence of a value
        for edge in self.models__from_edges():
            value_node = self.graph.node(edge.to_node_id())
            if isinstance(value_node, Model__MGraph__Json__Node__Value) and value_node.value == value:
                self.graph.delete_edge(edge.edge_id())
                return True
        return False