from typing                                                                      import Optional, Dict, Any
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node                  import Domain__MGraph__Json__Node
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node__Dict             import Model__MGraph__Json__Node__Dict
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__Property       import Schema__MGraph__Json__Node__Property
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__Property__Data import Schema__MGraph__Json__Node__Property__Data
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__Value          import Schema__MGraph__Json__Node__Value
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__Value__Data    import Schema__MGraph__Json__Node__Value__Data


class Domain__MGraph__Json__Node__Dict(Domain__MGraph__Json__Node):
    node: Model__MGraph__Json__Node__Dict                                                         # Reference to dict node model

    def properties(self) -> Dict[str, Any]:
        result = {}
        for edge in self.models__from_edges():
            property_node = self.model__node_from_edge(edge)
            if property_node.data.node_type != Schema__MGraph__Json__Node__Property:
                continue

            for value_edge in self.graph.edges():                                           # todo: see why we need to use self.graph.edges()
                if value_edge.from_node_id() == property_node.node_id:
                    value_node = self.graph.node(value_edge.to_node_id())
                    if value_node.data.node_type == Schema__MGraph__Json__Node__Value:              # todo: there is an interest case here, what happens if there is more than one Schema__MGraph__Json__Node__Value per Schema__MGraph__Json__Node__Property
                        result[property_node.data.node_data.name] = value_node.data.node_data.value # todo: solve issue of value not being recognized here
                        break
        return result

    def property(self, name: str) -> Optional[Any]:                                                                     # Get value of a property by name
        props = self.properties()
        return props.get(name)

    def add_property(self, name: str, value: Any) -> None:                                                              # Add or update a property
        # Find existing property node if any
        for edge in self.models__from_edges():
            property_node = self.model__node_from_edge(edge)
            if property_node.data.node_type == Schema__MGraph__Json__Node__Property:
                if property_node.data.node_data.name == name:
                    for value_edge in self.graph.node__from_edges(property_node.node_id):

                        value_node = self.graph.node(value_edge.to_node_id())
                        if value_node.data.node_type is Schema__MGraph__Json__Node__Value:
                            value_node.data.node_data.value = value
                            return

        # Create new property node and value node

        property_name__schema__node_data = Schema__MGraph__Json__Node__Property__Data(name      = name )
        property_name__schema__node      = Schema__MGraph__Json__Node__Property      (node_data = property_name__schema__node_data)
        property_name__model__node       = self.graph.add_node                       (node      = property_name__schema__node     )

        property_value__schema__node_data = Schema__MGraph__Json__Node__Value__Data  (value     = value, value_type=type(value)      )
        property_value__node_value       = Schema__MGraph__Json__Node__Value         (node_data = property_value__schema__node_data  )
        property_value__model__node      = self.graph.add_node                       (node      = property_value__node_value          )

        self.graph.new_edge(from_node_id=self.node_id                      , to_node_id=property_name__model__node.node_id )
        self.graph.new_edge(from_node_id=property_name__model__node.node_id, to_node_id=property_value__model__node.node_id)

    def update(self, properties: Dict[str, Any]) -> None:                       # Bulk update multiple properties
        for name, value in properties.items():
            self.add_property(name, value)

    def delete_property(self, name: str) -> bool:
        """Remove a property by name"""
        for edge in self.models__from_edges():
            property_node = self.model__node_from_edge(edge)
            if property_node.data.node_type == Schema__MGraph__Json__Node__Property:
                if property_node.data.node_data.name == name:
                    self.graph.delete_edge(edge.edge_id     ())
                    self.graph.delete_node(edge.to_node_id  ())                         # todo: BUG we also need to delete the value node
                    return True
        return False