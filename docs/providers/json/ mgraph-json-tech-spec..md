# MGraph JSON Provider Technical Specification

## Overview

The JSON Provider will enable MGraph to ingest, manipulate, and export JSON data structures using MGraph's core graph capabilities. This document outlines the technical approach, architecture, and implementation details.

## Core Concept: A Graph-Native Approach

The JSON Provider implements a pure graph-native approach to JSON representation, where every single JSON element becomes a node in its own right. This aligns perfectly with graph thinking and MGraph's core principles.

Key Principles:
- Every JSON element (value, object, array) is a node
- Structure is maintained purely through edges
- No special property nodes or complex containers needed
- Natural graph traversal and transformation
- Maximum simplicity and flexibility

## Architecture

### Three-Layer Architecture

Following MGraph's architectural principles, the implementation is divided into three clean layers:

```mermaid
classDiagram
    %% Schema Layer
    class Schema__Json__Node__Type {
        <<enumeration>>
        VALUE
        DICT
        LIST
    }
    
    class Schema__Json__Node__Data {
        +value: Any
        +node_type: Schema__Json__Node__Type
    }
    
    class Schema__Json__Node {
        +node_data: Schema__Json__Node__Data
    }
    
    %% Model Layer
    class Model__Json__Node {
        +data: Schema__Json__Node
        +is_value()
        +is_dict()
        +is_list()
        +get_value()
    }
    
    %% Domain Layer
    class Domain__Json__Node {
        +node: Model__Json__Node
        +graph: Model__Json__Graph
    }

    Schema__Json__Node__Data -- Schema__Json__Node__Type
    Schema__Json__Node *-- Schema__Json__Node__Data
    Model__Json__Node *-- Schema__Json__Node
    Domain__Json__Node *-- Model__Json__Node
```

Each layer has clear responsibilities:
- **Schema Layer**: Pure data structures and type definitions
- **Model Layer**: Operations on single entities
- **Domain Layer**: High-level JSON operations and business logic

### Node Types

The system recognizes three fundamental node types:

```python
class Schema__Json__Node__Type(Enum):
    VALUE = "value"    # Primitive values (str, int, bool, None)
    DICT  = "dict"     # JSON objects {}
    LIST  = "list"     # JSON arrays []

class Schema__Json__Node__Data(Type_Safe):
    value    : Any                           # The actual value for VALUE nodes
    node_type: Schema__Json__Node__Type      # Type of this node
```

This minimal structure captures all possible JSON structures while maintaining pure graph principles. Each node is self-contained and requires no special handling or complex containers.

## JSON to Graph Mapping

In our graph-native approach, every JSON element becomes a node, creating a pure graph structure. 

### Examples

1. **Simple Object**:
   ```json
   {
     "name": "John"
   }
   ```
   Becomes three nodes:
   ```
   [DICT node] --> [VALUE node: "name"] --> [VALUE node: "John"]
   ```

2. **Array**:
   ```json
   ["a", "b"]
   ```
   Becomes three nodes:
   ```
   [LIST node] --> [VALUE node: "a"]
                   [VALUE node: "b"]
   ```
   Edge order preserves array ordering.

3. **Nested Structures**:
   ```json
   {
     "user": {
       "details": {
         "age": 30
       }
     }
   }
   ```
   Becomes:
   ```
   [root] --has_property--> [user] --has_property--> [details] --has_property--> [age: 30]
   ```

### Node and Edge Patterns

The system uses a minimal set of concepts:

**Node Types:**
| Type  | Purpose | Contains |
|-------|---------|----------|
| VALUE | Represents any JSON value | The actual value (string, number, bool, null) |
| DICT  | Represents JSON objects | Nothing (structure through edges) |
| LIST  | Represents JSON arrays | Nothing (structure through edges) |

**Edge Usage:**
- Edges maintain structure and order
- No special edge types needed
- Array order preserved through edge metadata
- Object property names stored in VALUE nodes

## Implementation Details

### 1. Core Classes

```python
class MGraph__Json:
    """Main provider class for JSON operations"""
    
    def load(self, json_data: Union[str, dict]) -> Domain__Json__Graph:
        """Load JSON data into graph structure"""
        
    def export(self, format: str = 'json') -> Union[dict, str]:
        """Export graph to specified format"""

class Schema__Json__Node__Data:
    """Extended node data for JSON values"""
    json_value: Any
    json_type: str
    json_key: Optional[str]

class Domain__Json__Graph(Domain__MGraph__Graph):
    """Domain-specific graph operations for JSON"""
    
    def query_json_path(self, path: str) -> Any:
        """Query graph using JSON path syntax"""
```

### 2. Key Operations

#### Loading JSON
1. Parse JSON input
2. Create root node
3. Recursively process structure
4. Create nodes for values
5. Create edges for relationships

```python
def _process_json(self, data: Any, parent_node: Schema__Json__Node) -> None:
    if isinstance(data, dict):
        self._process_object(data, parent_node)
    elif isinstance(data, list):
        self._process_array(data, parent_node)
    else:
        self._process_primitive(data, parent_node)
```

#### Exporting JSON
1. Start from root node
2. Recursively rebuild structure
3. Handle circular references
4. Generate output format

### 3. Special Cases

| Case | Handling Strategy |
|------|------------------|
| Circular References | Track visited nodes, create reference edges |
| Large Arrays | Lazy loading for arrays over threshold size |
| Deep Nesting | Implement depth limit with warning |
| Schema Validation | Optional JSON Schema validation during load |

## Usage Examples

### Basic Usage
```python
# Create provider
json_provider = MGraph__Json()

# Load JSON
with open('data.json') as f:
    graph = json_provider.load(f.read())

# Manipulate
with graph.edit() as edit:
    node = edit.query_json_path('$.users[0].name')
    node.set_value('New Name')

# Export
result = json_provider.export()
```

### Advanced Features
```python
# Query with JSON Path
users = graph.query_json_path('$.users[*].name')

# Export to different format
rdf = json_provider.export(format='rdf')
xml = json_provider.export(format='xml')
```

## Implementation Phases

1. **Phase 1: Core Implementation**
   - Basic JSON loading
   - Simple object/array handling
   - Primitive value support
   - JSON export

2. **Phase 2: Advanced Features**
   - JSON Path queries
   - Circular reference handling
   - Performance optimizations
   - Large dataset support

3. **Phase 3: Format Support**
   - RDF export
   - XML export
   - Other format support

## Testing Strategy

1. **Unit Tests**
   - Individual component testing
   - Edge case validation
   - Type conversion verification

2. **Integration Tests**
   - End-to-end workflows
   - Format conversion accuracy
   - Performance benchmarks

3. **Validation Tests**
   - JSON Schema compliance
   - Circular reference handling
   - Deep nesting scenarios

## Success Criteria

1. **Functionality**
   - Accurate JSON representation
   - Lossless round-trip conversion
   - Efficient graph operations

2. **Performance**
   - Linear time complexity for basic operations
   - Efficient memory usage
   - Scalable with large datasets

3. **Usability**
   - Simple, intuitive API
   - Clear error messages
   - Comprehensive documentation

## Next Steps

1. Implement Schema__Json__Node__Data
2. Create basic JSON loading functionality
3. Implement graph to JSON export
4. Add JSON Path query support
5. Develop format conversion capabilities