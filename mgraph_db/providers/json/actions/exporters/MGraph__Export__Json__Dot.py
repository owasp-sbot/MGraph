from typing                                                                 import Dict, Any, List
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__Property   import Domain__MGraph__Json__Node__Property
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__Dict        import Model__MGraph__Json__Node__Dict
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__List        import Model__MGraph__Json__Node__List
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__Value       import Model__MGraph__Json__Node__Value
from mgraph_db.providers.json.actions.exporters.MGraph__Json__Export__Base  import MGraph__Export__Json__Base, Export__Json__Node_Type, Export__Json__Relation_Type
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__Dict       import Domain__MGraph__Json__Node__Dict
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__List       import Domain__MGraph__Json__Node__List
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__Value      import Domain__MGraph__Json__Node__Value

class MGraph__Export__Json__Dot(MGraph__Export__Json__Base):                                     # DOT format exporter for graph visualization

    def get_node_style(self, node_type: str) -> Dict[str, str]:                 # Get DOT styling attributes for node types
        styles = {
            Export__Json__Node_Type.OBJECT: {
                'shape': 'record',
                'style': 'filled',
                'fillcolor': 'lightblue'
            },
            Export__Json__Node_Type.PROPERTY: {
                'shape': 'ellipse',
                'style': 'filled',
                'fillcolor': 'lightgreen'
            },
            Export__Json__Node_Type.VALUE: {
                'shape': 'box',
                'style': 'filled',
                'fillcolor': 'lightyellow'
            },
            Export__Json__Node_Type.ARRAY: {
                'shape': 'record',
                'style': 'filled',
                'fillcolor': 'lightpink'
            }
        }
        return styles.get(node_type, {})

    def format_node_attributes(self, attributes: Dict[str, str]) -> str:         # Format node attributes for DOT syntax
        if not attributes:
            return ""
        attrs = [f'{k}="{v}"' for k, v in attributes.items()]
        return f" [{', '.join(attrs)}]"

    def format_value(self, value: Any) -> str:                                    # Format values specifically for DOT format with proper escaping
        if value is None:
            return "null"
        if isinstance(value, bool):
            return str(value).lower()
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, str):                                                # dot specific escaping
            escaped = value.replace('"', '\\"')
            return f'{escaped}'
        #return f'"{value}"'
        
    def process_node(self, node: Any) -> str:                                    # Process a node and generate DOT representation
        node_type = self.get_node_type(node)
        node_id = self.generate_node_id(node_type.lower())

        attributes = self.get_node_style(node_type)

        if isinstance(node, Domain__MGraph__Json__Node__Value):
            attributes['label'] = self.format_value(node.value)
        elif isinstance(node, Domain__MGraph__Json__Node__Dict):
            attributes['label'] = "object"
        elif isinstance(node, Domain__MGraph__Json__Node__List):
            attributes['label'] = "array"

        self.context['nodes'][node_id] = {
            'type': node_type,
            'attributes': attributes
        }

        return node_id

    def process_edge(self, from_id: str, to_id: str, type_: str) -> None:       # Process an edge and generate DOT representation
        edge_id = self.generate_node_id('edge')

        self.context['edges'][edge_id] = { 'from': from_id,
                                           'to'    : to_id,
                                           'type': type_,
                                           'attributes': {  'label': type_ } }

    def process_value_node(self, node: Domain__MGraph__Json__Node__Value) -> str:  # Process a value node
        return self.process_node(node)

    def process_array_node(self, node: Domain__MGraph__Json__Node__List) -> str:
        """Process an array node by traversing its existing graph structure"""
        array_id = self.process_node(node)

        # Get outgoing edges from the array node to its items
        for edge in node.models__from_edges():
            # Get the model node for this edge
            model_node = node.model__node_from_edge(edge)
            child_id   = None
            # Create appropriate domain node based on model type
            if isinstance(model_node, Model__MGraph__Json__Node__Dict):
                child_node = Domain__MGraph__Json__Node__Dict(node=model_node, graph=self.graph.model)
                child_id = self.process_object_node(child_node)
            elif isinstance(model_node, Model__MGraph__Json__Node__List):
                child_node = Domain__MGraph__Json__Node__List(node=model_node, graph=self.graph.model)
                child_id = self.process_array_node(child_node)
            elif isinstance(model_node, Model__MGraph__Json__Node__Value):
                child_node = Domain__MGraph__Json__Node__Value(node=model_node, graph=self.graph.model)
                child_id = self.process_value_node(child_node)


            self.process_edge(array_id, child_id, Export__Json__Relation_Type.ARRAY_ITEM)

        return array_id

    def process_object_node(self, node: Domain__MGraph__Json__Node__Dict) -> str:
        """Process an object node by traversing its existing graph structure"""
        object_id = self.process_node(node)

        # Get outgoing edges from the object node to properties
        for edge in node.models__from_edges():
            # Get the property node
            property_model = node.model__node_from_edge(edge)
            property_node = Domain__MGraph__Json__Node__Property(node=property_model, graph=self.graph.model)

            # Process property node
            prop_id = self.generate_node_id('property')
            self.context['nodes'][prop_id] = {
                'type': Export__Json__Node_Type.PROPERTY,
                'attributes': {
                    **self.get_node_style(Export__Json__Node_Type.PROPERTY),
                    'label': property_node.name
                }
            }

            self.process_edge(object_id, prop_id, Export__Json__Relation_Type.HAS_PROPERTY)

            # Get the value node connected to this property
            for value_edge in property_node.models__from_edges():
                value_model = property_node.model__node_from_edge(value_edge)
                value_id    = None
                # Create appropriate domain node based on model type
                if isinstance(value_model, Model__MGraph__Json__Node__Dict):
                    value_node = Domain__MGraph__Json__Node__Dict(node=value_model, graph=self.graph.model)
                    value_id = self.process_object_node(value_node)
                elif isinstance(value_model, Model__MGraph__Json__Node__List):
                    value_node = Domain__MGraph__Json__Node__List(node=value_model, graph=self.graph.model)
                    value_id = self.process_array_node(value_node)
                elif isinstance(value_model, Model__MGraph__Json__Node__Value):
                    value_node = Domain__MGraph__Json__Node__Value(node=value_model, graph=self.graph.model)
                    value_id = self.process_value_node(value_node)

                self.process_edge(prop_id, value_id, Export__Json__Relation_Type.HAS_VALUE)

        return object_id

    def format_output(self) -> str:                                              # Generate the final DOT format output
        lines = ['digraph {']

        lines.append('  // Graph settings')
        lines.append('  graph [rankdir=LR]')
        lines.append('  node [fontname="Arial"]')
        lines.append('  edge [fontname="Arial"]')
        lines.append('')

        lines.append('  // Nodes')
        for node_id, node_data in self.context['nodes'].items():
            attributes = self.format_node_attributes(node_data['attributes'])
            lines.append(f'  "{node_id}"{attributes}')

        if self.context['nodes']:
            lines.append('')

        lines.append('  // Edges')
        for edge_id, edge_data in self.context['edges'].items():
            attributes = self.format_node_attributes(edge_data['attributes'])
            lines.append(f'  "{edge_data["from"]}" -> "{edge_data["to"]}"{attributes}')

        lines.append('}')
        return '\n'.join(lines)