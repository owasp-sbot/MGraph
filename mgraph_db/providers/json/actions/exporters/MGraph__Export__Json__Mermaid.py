from typing                                                                 import Dict, Any
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__Property   import Domain__MGraph__Json__Node__Property
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__Dict        import Model__MGraph__Json__Node__Dict
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__List        import Model__MGraph__Json__Node__List
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__Value       import Model__MGraph__Json__Node__Value
from mgraph_db.providers.json.actions.exporters.MGraph__Json__Export__Base  import MGraph__Export__Json__Base, Export__Json__Node_Type, Export__Json__Relation_Type
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__Dict       import Domain__MGraph__Json__Node__Dict
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__List       import Domain__MGraph__Json__Node__List
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__Value      import Domain__MGraph__Json__Node__Value

class MGraph__Export__Json__Mermaid(MGraph__Export__Json__Base):                                    # Mermaid format exporter for graph visualization

    # todo add support for shape, which needs to happen at node creation not style
    def get_node_style(self, node_type: str) -> Dict[str, str]:                                     # Get Mermaid styling attributes for node types
        styles = {
            Export__Json__Node_Type.OBJECT: {
                'shape'     : 'rect'    ,                                                            # Rectangle shape for objects
                'style'     : 'default' ,                                                            # Default style
                'fill'      : '#BBDEFB' ,                                                            # Light blue fill
                'stroke'    : '#1976D2'                                                              # Darker blue border
            },
            Export__Json__Node_Type.PROPERTY: {
                'shape'     : 'stadium' ,                                                            # Rounded rectangle for properties
                'style'     : 'default' ,
                'fill'      : '#C8E6C9' ,                                                            # Light green fill
                'stroke'    : '#388E3C'                                                              # Darker green border
            },
            Export__Json__Node_Type.VALUE: {
                'shape'     : 'square'  ,                                                            # Square shape for values
                'style'     : 'default' ,
                'fill'      : '#FFF9C4' ,                                                            # Light yellow fill
                'stroke'    : '#FBC02D'                                                              # Darker yellow border
            },
            Export__Json__Node_Type.ARRAY: {
                'shape'     : 'rect'    ,                                                            # Rectangle shape for arrays
                'style'     : 'default' ,
                'fill'      : '#F8BBD0' ,                                                            # Light pink fill
                'stroke'    : '#C2185B'                                                              # Darker pink border
            }
        }
        return styles.get(node_type, {})


    def format_value(self, value: Any) -> str:                                                       # Format values specifically for Mermaid format
        if value is None:
            return "null"
        if isinstance(value, bool):
            return str(value).lower()
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, str):
            escaped = value.replace('"', '\\"').replace('\\n', '<br/>')                              # Handle newlines for Mermaid
            return f'{escaped}'

    def process_node(self, node: Any) -> str:                                                        # Process a node and generate Mermaid representation
        node_type = self.get_node_type(node)
        node_id = self.generate_node_id(node_type.lower())

        style_attrs = self.get_node_style(node_type)
        label = ""

        if isinstance(node, Domain__MGraph__Json__Node__Value):
            label = self.format_value(node.value)
        elif isinstance(node, Domain__MGraph__Json__Node__Dict):
            label = "object"
        elif isinstance(node, Domain__MGraph__Json__Node__List):
            label = "array"

        attributes = {
            'label': label,
            'style': f"fill:{style_attrs['fill']},stroke:{style_attrs['stroke']}"
        }

        self.context['nodes'][node_id] = {
            'type'       : node_type  ,
            'attributes': attributes
        }

        return node_id

    def process_edge(self, from_id: str, to_id: str, type_: str) -> None:                           # Process an edge and generate Mermaid representation
        edge_id = self.generate_node_id('edge')

        # Define edge styles based on relationship type
        edge_styles = {
            Export__Json__Relation_Type.HAS_PROPERTY: '-->',                                         # Solid line for property relations
            Export__Json__Relation_Type.HAS_VALUE   : '-->',                                         # Arrow for value relations
            Export__Json__Relation_Type.ARRAY_ITEM  : '==>'                                          # Thick arrow for array items
        }

        edge_style = edge_styles.get(type_, '-->')                                                   # Default to normal arrow if type unknown

        self.context['edges'][edge_id] = {
            'from'       : from_id    ,
            'to'         : to_id      ,
            'type'       : type_      ,
            'edge_style' : edge_style ,
            'attributes' : {'label'   : type_}
        }

    def process_value_node(self, node: Domain__MGraph__Json__Node__Value) -> str:                    # Process a value node
        return self.process_node(node)

    def process_array_node(self, node: Domain__MGraph__Json__Node__List) -> str:                     # Process an array node by traversing its graph structure
        array_id = self.process_node(node)

        for edge in node.models__from_edges():
            model_node = node.model__node_from_edge(edge)
            child_id  = None

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
                self.process_edge(array_id, child_id, Export__Json__Relation_Type.ARRAY_ITEM)

        return array_id

    def process_object_node(self, node: Domain__MGraph__Json__Node__Dict) -> str:                    # Process an object node by traversing its graph structure
        object_id = self.process_node(node)

        for edge in node.models__from_edges():
            property_model = node.model__node_from_edge(edge)
            property_node = Domain__MGraph__Json__Node__Property(node=property_model, graph=self.graph.model)

            prop_id        = self.generate_node_id('property')
            property_style = self.get_node_style(Export__Json__Node_Type.PROPERTY)

            self.context['nodes'][prop_id] = {
                'type'      : Export__Json__Node_Type.PROPERTY,
                'attributes': {
                    'style': f"fill:{property_style['fill']},stroke:{property_style['stroke']}",
                    'label': property_node.name
                }
            }


            self.process_edge(object_id, prop_id, Export__Json__Relation_Type.HAS_PROPERTY)

            for value_edge in property_node.models__from_edges():
                value_model = property_node.model__node_from_edge(value_edge)
                value_id   = None

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

    def format_output(self) -> str:                                                                  # Generate the final Mermaid format output
        lines = ['flowchart LR']                                                                     # Left to right flowchart

        # Add nodes without styles
        for node_id, node_data in self.context['nodes'].items():
            lines.append(f'    {node_id}[{node_data["attributes"].get("label", "")}]')

        if self.context['nodes']:
            lines.append('')

        # Add edges
        for edge_id, edge_data in self.context['edges'].items():
            edge_style = edge_data['edge_style']
            label = edge_data['attributes'].get('label', '')
            if label:
                label = f'|{label}|'
            lines.append(f'    {edge_data["from"]} {edge_style}{label} {edge_data["to"]}')

        if self.context['edges']:
            lines.append('')

        # Add styles at the end
        for node_id, node_data in self.context['nodes'].items():
            attributes       = node_data.get('attributes', {})
            attributes_style = attributes.get('style', '')
            if attributes_style:
                lines.append(f'    style {node_id} {attributes_style}')

        return '\n'.join(lines)