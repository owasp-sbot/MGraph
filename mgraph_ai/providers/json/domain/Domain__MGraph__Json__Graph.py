from typing                                                             import Any, Optional
from mgraph_ai.mgraph.domain.Domain__MGraph__Graph                      import Domain__MGraph__Graph
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Types        import Domain__MGraph__Json__Types
from mgraph_ai.providers.json.models.Model__MGraph__Json__Graph         import Model__MGraph__Json__Graph
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node         import Domain__MGraph__Json__Node
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node__Dict   import Domain__MGraph__Json__Node__Dict
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node__List   import Domain__MGraph__Json__Node__List
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node__Value  import Domain__MGraph__Json__Node__Value
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node        import Schema__MGraph__Json__Node


class Domain__MGraph__Json__Graph(Domain__MGraph__Graph):
    domain_types : Domain__MGraph__Json__Types
    model        : Model__MGraph__Json__Graph

    def root(self) -> Domain__MGraph__Json__Node:                                                # Get root node
        """Get the root node, creating it if it doesn't exist"""
        if not self.model.data.graph_data.root_id:
            schema_node = Schema__MGraph__Json__Node()                                           # Create basic root node
            node = self.model.add_node(schema_node)
            self.model.data.graph_data.root_id = node.node_id
            return Domain__MGraph__Json__Node(node=node, graph=self.model)

        root_model = self.model.node(self.model.data.graph_data.root_id)
        if not root_model:
            raise ValueError("Root node ID exists but node not found")

        return Domain__MGraph__Json__Node(node=root_model, graph=self.model)

    def root_content(self) -> Optional[Domain__MGraph__Json__Node]:                             # Get the content node
        """Get the content node attached to root (if any)"""
        root = self.root()
        edges = self.model.node__from_edges(root.node_id)
        if not edges:
            return None

        content_node = self.model.node(edges[0].to_node_id())                                   # Get first child

        # Return appropriate domain node type
        if isinstance(content_node.data, Schema__MGraph__Json__Node__Dict):
            return Domain__MGraph__Json__Node__Dict(node=content_node, graph=self.model)
        elif isinstance(content_node.data, Schema__MGraph__Json__Node__List):
            return Domain__MGraph__Json__Node__List(node=content_node, graph=self.model)
        elif isinstance(content_node.data, Schema__MGraph__Json__Node__Value):
            return Domain__MGraph__Json__Node__Value(node=content_node, graph=self.model)

        return None

    def set_root_content(self, data: Any) -> Domain__MGraph__Json__Node:                        # Set content node
        """Set the JSON content, creating appropriate node type"""
        root = self.root()

        # Remove any existing content
        edges = self.model.node__from_edges(root.node_id)
        for edge in edges:
            self.model.delete_edge(edge.edge_id())
            self.model.delete_node(edge.to_node_id())

        # Create appropriate node type for new content
        if isinstance(data, dict):
            content = self.new_dict_node(data)
        elif isinstance(data, (list, tuple)):
            content = self.new_list_node(data)
        else:
            content = self.new_value_node(data)

        # Link content to root
        self.model.new_edge(from_node_id=root.node_id, to_node_id=content.node_id)
        return content

    def new_dict_node(self, properties=None) -> Domain__MGraph__Json__Node__Dict:              # Create dictionary node
        """Create a new dictionary node with optional initial properties"""
        schema_node = Schema__MGraph__Json__Node__Dict()
        node = self.model.add_node(schema_node)
        dict_node = Domain__MGraph__Json__Node__Dict(node=node, graph=self.model)

        if properties:
            dict_node.update(properties)

        return dict_node

    def new_list_node(self, items=None) -> Domain__MGraph__Json__Node__List:                  # Create list node
        """Create a new list node with optional initial items"""
        schema_node = Schema__MGraph__Json__Node__List()
        node = self.model.add_node(schema_node)
        list_node = Domain__MGraph__Json__Node__List(node=node, graph=self.model)

        if items:
            list_node.extend(items)

        return list_node

    def new_value_node(self, value: Any) -> Domain__MGraph__Json__Node__Value:                # Create value node
        """Create a new value node with the given value"""
        node_data = Schema__MGraph__Json__Node__Value__Data(value=value, value_type=type(value))
        schema_node = Schema__MGraph__Json__Node__Value(node_data=node_data)
        node = self.model.add_node(schema_node)
        return Domain__MGraph__Json__Node__Value(node=node, graph=self.model)