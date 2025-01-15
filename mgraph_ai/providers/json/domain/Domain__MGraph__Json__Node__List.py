from typing                                                                   import List, Any, Union
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node               import Domain__MGraph__Json__Node
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node__Dict         import Domain__MGraph__Json__Node__Dict
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node__List          import Model__MGraph__Json__Node__List
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__Dict        import Schema__MGraph__Json__Node__Dict
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__List        import Schema__MGraph__Json__Node__List
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__Value       import Schema__MGraph__Json__Node__Value
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__Value__Data import \
    Schema__MGraph__Json__Node__Value__Data


class Domain__MGraph__Json__Node__List(Domain__MGraph__Json__Node):
    node: Model__MGraph__Json__Node__List                                    # Reference to list node model

    def items(self) -> List[Any]:                                           # Get all items in the list
        items = []
        for edge in self.models__from_edges():
            target_node = self.model__node_from_edge(edge)

            # Handle different node types
            if target_node.data.node_type == Schema__MGraph__Json__Node__Value:
                items.append(target_node.data.node_data.value)
            elif target_node.data.node_type == Schema__MGraph__Json__Node__Dict:
                # For dict nodes, get their properties
                dict_node = Domain__MGraph__Json__Node__Dict(node=target_node, graph=self.graph)
                items.append(dict_node.properties())
            elif target_node.data.node_type == Schema__MGraph__Json__Node__List:
                # For list nodes, recursively get their items
                list_node = Domain__MGraph__Json__Node__List(node=target_node, graph=self.graph)
                items.append(list_node.items())
        return items

    def add(self, value: Any) -> None:
        """Add an item to the list. The item can be a primitive value, dict, or list."""
        if isinstance(value, (str, int, float, bool)) or value is None:
            # Handle primitive values
            node_data   = Schema__MGraph__Json__Node__Value__Data(value=value, value_type=type(value))
            schema_node = Schema__MGraph__Json__Node__Value      (node_data=node_data)
            value_node  = self.graph.add_node(schema_node)

        elif isinstance(value, dict):
            # Handle dictionaries
            dict_node = Schema__MGraph__Json__Node__Dict()
            value_node = self.graph.add_node(dict_node)
            domain_dict = Domain__MGraph__Json__Node__Dict(node=value_node, graph=self.graph)
            domain_dict.update(value)

        elif isinstance(value, (list, tuple)):
            # Handle lists
            list_node = Schema__MGraph__Json__Node__List()
            value_node = self.graph.add_node(list_node)
            domain_list = Domain__MGraph__Json__Node__List(node=value_node, graph=self.graph)
            for item in value:
                domain_list.add(item)
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")

        print()
        print("from_node_id = ", self.node.node_id, " | to_node_id=", value_node.node_id)
        # Connect the new node to this list
        #self.graph.new_edge(from_node_id=self.node.node_id, to_node_id=value_node.node_id)

    def clear(self) -> None:                                               # Remove all items
        for edge in self.models__from_edges():
            target_node = self.model__node_from_edge(edge)
            self.graph.delete_edge(edge.edge_id())
            self.graph.delete_node(target_node.node_id())

    def extend(self, items: List[Any]) -> None:
        """Add multiple items to the list"""
        for item in items:
            self.add(item)

    def remove(self, value: Any) -> bool:                                 # Remove first occurrence of a value
        for edge in self.models__from_edges():
            target_node = self.model__node_from_edge(edge)
            if target_node.data.node_type == Schema__MGraph__Json__Node__Value:
                if target_node.data.node_data.value == value:
                    self.graph.delete_edge(edge.edge_id())
                    self.graph.delete_node(target_node.node_id())
                    return True
        return False