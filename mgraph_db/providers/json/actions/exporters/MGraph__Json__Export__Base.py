from typing                                                             import Dict, Any, Optional
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__Dict   import Domain__MGraph__Json__Node__Dict
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__List   import Domain__MGraph__Json__Node__List
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__Value  import Domain__MGraph__Json__Node__Value
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Graph        import Domain__MGraph__Json__Graph
from osbot_utils.utils.Files                                            import file_save

class Export__Json__Node_Type:                                                      # Node types in the graph
    OBJECT   = "object"    # JSON objects
    PROPERTY = "property"  # Object properties
    VALUE    = "value"     # Primitive values
    ARRAY    = "array"     # Array containers

class Export__Json__Value_Type:                                                     # Value types for JSON
    STRING  = "string"
    NUMBER  = "number"
    BOOLEAN = "boolean"
    NULL    = "null"

class Export__Json__Relation_Type:                                                  # Relationship types between nodes
    HAS_PROPERTY = "has_property"  # Object to property
    HAS_VALUE    = "has_value"     # Property to value
    ARRAY_ITEM   = "array_item"    # Array to item

class Export__Json__Format_Error(Exception):                                        # Base class for format-specific export errors
    pass

class MGraph__Export__Json__Base:                                                          # Base class for format-specific exporters

    def __init__(self, graph: Domain__MGraph__Json__Graph):                       # Initialize with graph
        self.graph = graph
        self.context = self.init_context()

    def init_context(self) -> Dict:                                               # Initialize format-specific export context
        return {
            'nodes': {},            # Stores processed nodes
            'edges': {},            # Stores processed edges
            'counters': {           # ID counters for different node types
                'node': 0,
                'edge': 0,
                'property': 0,
                'value': 0,
                'array': 0
            }
        }

    def generate_node_id(self, prefix: str) -> str:                              # Generate format-friendly node IDs
        counter = self.context['counters'].get(prefix, 0)
        self.context['counters'][prefix] = counter + 1
        return f"{prefix}_{counter}"

    def format_value(self, value: Any) -> str:                                   # Format values consistently across exports
        if value is None:
            return "null"
        if isinstance(value, bool):
            return str(value).lower()
        if isinstance(value, (int, float)):
            return str(value)
        return f'"{value}"'  # strings

    def get_node_type(self, node: Any) -> str:                                   # Determine node type based on instance
        if isinstance(node, Domain__MGraph__Json__Node__Dict):
            return Export__Json__Node_Type.OBJECT
        if isinstance(node, Domain__MGraph__Json__Node__List):
            return Export__Json__Node_Type.ARRAY
        if isinstance(node, Domain__MGraph__Json__Node__Value):
            return Export__Json__Node_Type.VALUE
        return Export__Json__Node_Type.PROPERTY

    def process_node(self, node: Any) -> str:                                    # Process a node and return its ID
        raise NotImplementedError()

    def process_edge(self, from_id: str, to_id: str, type_: str) -> None:       # Process an edge between nodes
        raise NotImplementedError()

    def process_value_node(self, node: Domain__MGraph__Json__Node__Value) -> str:  # Process a value node
        raise NotImplementedError()

    def process_array_node(self, node: Domain__MGraph__Json__Node__List) -> str:   # Process an array node
        raise NotImplementedError()

    def process_object_node(self, node: Domain__MGraph__Json__Node__Dict) -> str:  # Process an object node
        raise NotImplementedError()

    def format_output(self) -> str:                                              # Format the final output
        raise NotImplementedError()

    def print(self):
        print()
        print()
        self.context = self.init_context()
        str_output = self.to_string()
        print(str_output)

    def to_string(self, **options) -> str:                                       # Convert graph to format-specific string
        root_content = self.graph.root_content()
        if not root_content:
            return ""

        try:
            if isinstance(root_content, Domain__MGraph__Json__Node__Dict):
                self.process_object_node(root_content)
            elif isinstance(root_content, Domain__MGraph__Json__Node__List):
                self.process_array_node(root_content)
            elif isinstance(root_content, Domain__MGraph__Json__Node__Value):
                self.process_value_node(root_content)

            return self.format_output()
        except Exception as e:
            raise Export__Json__Format_Error(f"Export failed: {str(e)}")

    def to_file(self, file_path: str, **options) -> bool:                        # Export graph to file
        try:
            output = self.to_string(**options)
            if output:
                file_save(contents=output, path=file_path)
                return True
            return False
        except Exception as e:
            raise Export__Json__Format_Error(f"File export failed: {str(e)}")