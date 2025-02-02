from typing                                                                 import Dict, Any
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__Property   import Domain__MGraph__Json__Node__Property
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__Dict        import Model__MGraph__Json__Node__Dict
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__List        import Model__MGraph__Json__Node__List
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__Value       import Model__MGraph__Json__Node__Value
from mgraph_db.providers.json.actions.exporters.MGraph__Json__Export__Base  import MGraph__Export__Json__Base, Export__Json__Node_Type, Export__Json__Relation_Type
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__Dict       import Domain__MGraph__Json__Node__Dict
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__List       import Domain__MGraph__Json__Node__List
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__Value      import Domain__MGraph__Json__Node__Value

class MGraph__Export__Json__Cypher(MGraph__Export__Json__Base):                                    # Cypher format exporter for Neo4j

    def get_node_labels(self, node_type: str) -> str:                                             # Get Neo4j labels for node types
        labels = {
            Export__Json__Node_Type.OBJECT  : 'JsonObject'  ,                                     # Label for JSON objects
            Export__Json__Node_Type.PROPERTY: 'JsonProperty',                                     # Label for property nodes
            Export__Json__Node_Type.VALUE   : 'JsonValue'   ,                                     # Label for value nodes
            Export__Json__Node_Type.ARRAY   : 'JsonArray'                                         # Label for array nodes
        }
        return labels.get(node_type, 'Node')                                                      # Default to generic Node label

    def format_value(self, value: Any) -> str:                                                    # Format values for Cypher
        if value is None:
            return "null"
        if isinstance(value, bool):
            return str(value).lower()
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, str):                                                                # Escape quotes for Cypher
            escaped = value.replace('"', '\\"').replace("'", "\\'")
            return f"'{escaped}'"
        return f"'{value}'"

    def process_node(self, node: Any) -> str:                                                     # Process a node for Cypher output
        node_type = self.get_node_type(node)
        node_id = self.generate_node_id(node_type.lower())
        label = self.get_node_labels(node_type)

        properties = {}
        if isinstance(node, Domain__MGraph__Json__Node__Value):
            properties['value'] = node.value
            properties['valueType'] = type(node.value).__name__ if node.value is not None else 'null'
        elif isinstance(node, Domain__MGraph__Json__Node__Dict):
            properties['type'] = 'object'
        elif isinstance(node, Domain__MGraph__Json__Node__List):
            properties['type'] = 'array'
        elif isinstance(node, Domain__MGraph__Json__Node__Property):
            properties['name'] = node.name

        self.context['nodes'][node_id] = {
            'label': label,
            'properties': properties
        }

        return node_id

    def process_edge(self, from_id: str, to_id: str, type_: str) -> None:                        # Process edges for Cypher output
        edge_id = self.generate_node_id('edge')

        self.context['edges'][edge_id] = {
            'from': from_id,
            'to': to_id,
            'type': type_,
            'properties': {}
        }

    def process_value_node(self, node: Domain__MGraph__Json__Node__Value) -> str:                # Process value nodes
        return self.process_node(node)

    def process_array_node(self, node: Domain__MGraph__Json__Node__List) -> str:                 # Process array nodes
        array_id = self.process_node(node)

        for index, edge in enumerate(node.models__from_edges()):
            model_node = node.model__node_from_edge(edge)
            child_id = None

            if isinstance(model_node, Model__MGraph__Json__Node__Dict):
                child_node = Domain__MGraph__Json__Node__Dict(node=model_node, graph=self.graph.model)
                child_id = self.process_object_node(child_node)
            elif isinstance(model_node, Model__MGraph__Json__Node__List):
                child_node = Domain__MGraph__Json__Node__List(node=model_node, graph=self.graph.model)
                child_id = self.process_array_node(child_node)
            elif isinstance(model_node, Model__MGraph__Json__Node__Value):
                child_node = Domain__MGraph__Json__Node__Value(node=model_node, graph=self.graph.model)
                child_id = self.process_value_node(child_node)

            if child_id:
                edge_id = self.generate_node_id('edge')
                self.context['edges'][edge_id] = {
                    'from': array_id,
                    'to': child_id,
                    'type': Export__Json__Relation_Type.ARRAY_ITEM,
                    'properties': {'index': index}
                }

        return array_id

    def process_object_node(self, node: Domain__MGraph__Json__Node__Dict) -> str:                # Process object nodes
        object_id = self.process_node(node)

        for edge in node.models__from_edges():
            property_model = node.model__node_from_edge(edge)
            property_node = Domain__MGraph__Json__Node__Property(node=property_model, graph=self.graph.model)

            prop_id = self.generate_node_id('property')
            self.context['nodes'][prop_id] = {
                'label': self.get_node_labels(Export__Json__Node_Type.PROPERTY),
                'properties': {'name': property_node.name}
            }

            self.process_edge(object_id, prop_id, Export__Json__Relation_Type.HAS_PROPERTY)

            for value_edge in property_node.models__from_edges():
                value_model = property_node.model__node_from_edge(value_edge)
                value_id = None

                if isinstance(value_model, Model__MGraph__Json__Node__Dict):
                    value_node = Domain__MGraph__Json__Node__Dict(node=value_model, graph=self.graph.model)
                    value_id = self.process_object_node(value_node)
                elif isinstance(value_model, Model__MGraph__Json__Node__List):
                    value_node = Domain__MGraph__Json__Node__List(node=value_model, graph=self.graph.model)
                    value_id = self.process_array_node(value_node)
                elif isinstance(value_model, Model__MGraph__Json__Node__Value):
                    value_node = Domain__MGraph__Json__Node__Value(node=value_model, graph=self.graph.model)
                    value_id = self.process_value_node(value_node)

                if value_id:
                    self.process_edge(prop_id, value_id, Export__Json__Relation_Type.HAS_VALUE)

        return object_id

    def format_property_string(self, properties: Dict[str, Any]) -> str:                          # Format node/edge properties for Cypher
        if not properties:
            return ""
        props = [f"{k}: {self.format_value(v)}" for k, v in properties.items()]
        return f" {{ {', '.join(props)} }}"

    def format_output(self) -> str:
        lines = ['// Clear existing data',
                 'MATCH (n) DETACH DELETE n;',
                 '',
                 '// Create nodes']

        # Create nodes
        for node_id, node_data in self.context['nodes'].items():
            properties = node_data['properties']
            properties['id'] = node_id  # Add 'id' to the properties map
            lines.append(f"CREATE (:{node_data['label']} {self.format_property_string(properties)});")

        lines.append('')
        lines.append('// Create relationships')

        # Create relationships
        for edge_id, edge_data in self.context['edges'].items():
            properties = self.format_property_string(edge_data['properties'])
            lines.append(
                f"MATCH (from {{ id: '{edge_data['from']}' }}), " +
                f"(to {{ id: '{edge_data['to']}' }}) " +
                f"CREATE (from)-[:{edge_data['type']}{properties}]->(to);"
            )

        return '\n'.join(lines)
