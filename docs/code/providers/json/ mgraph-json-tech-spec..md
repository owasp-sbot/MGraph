# MGraph__Json Technical Specification

## Introduction

MGraph__Json is a powerful component of the MGraph system that enables graph-based manipulation of JSON data structures. It transforms JSON documents into graph representations while preserving their semantic relationships, allowing developers to perform complex operations that would be difficult or impossible with traditional JSON parsing methods.

This technical specification serves as both a reference guide and a template for implementing providers in the MGraph ecosystem. It documents the internal architecture, design patterns, and implementation details derived from the current source code, providing a foundation for understanding and extending the system.

### Quick Start Example

Here's a practical example showing MGraph__Json in action:

```python
# Create MGraph__Json instance and load JSON from a URL
mgraph_json = MGraph__Json()
json_data   = GET_json("https://api.example.com/data-feed")
mgraph_json.load().from_json(json_data)

# Perform graph operations
with mgraph_json.edit() as edit:
    root = edit.root()
    # Manipulate the data structure
    
# Export modified JSON
result = mgraph_json.export().to_dict()
```

Performance metrics from real-world usage (based on a feed with 1,400 nodes):
- JSON Fetch: ~0.5 seconds
- Graph Construction: ~2.0 seconds
- Total Processing: ~2.5 seconds

This demonstrates MGraph__Json's ability to handle substantial JSON documents while maintaining reasonable performance characteristics.

## Purpose and Use Cases

MGraph__Json converts a JSON file into a graph object based on nodes and edges.

By doing this MGraph__Json addresses several key challenges in JSON data handling:

1. **Complex Structure Manipulation**
   - Modify deeply nested JSON structures
   - Preserve relationships during transformations
   - Handle circular references

2. **Type Safety and Validation**
   - Ensure type consistency
   - Validate structural changes
   - Maintain JSON semantics

3. **Performance and Scale**
   - Handle large JSON documents
   - Support streaming operations
   - Enable partial document updates

4. **Data Integration**
   - Convert between JSON and graph representations
   - Preserve metadata and relationships
   - Support bidirectional transformation
   - Enable format-specific optimizations

## Overview

MGraph__Json serves as the primary interface for JSON document handling within the MGraph system. It implements a sophisticated graph-based representation of JSON data structures, enabling complex manipulations while preserving JSON semantics and relationships. The implementation follows MGraph's three-layer architecture pattern: Schema, Model, and Domain layers.

## Core Architecture

### Class Hierarchy

```
MGraph__Json
├── graph: Domain__MGraph__Json__Graph
├── data   () -> MGraph__Data
├── edit   () -> MGraph__Edit
├── export () -> MGraph__Json__Export
├── load   () -> MGraph__Json__Load
└── storage() -> MGraph__Storage
```

The main class provides access to five primary operation categories through its methods, each returning specialized operation handlers.

### Layer Implementation

#### Schema Layer

The Schema layer defines the core data structures and type definitions:

1. **Node Types**:
   - `Schema__MGraph__Json__Node`          : Base node class
   - `Schema__MGraph__Json__Node__Dict`    : JSON object nodes
   - `Schema__MGraph__Json__Node__List`    : JSON array nodes
   - `Schema__MGraph__Json__Node__Value`   : Primitive value nodes
   - `Schema__MGraph__Json__Node__Property`: Property name nodes

2. **Edge Type**:
   - `Schema__MGraph__Json__Edge`: Represents relationships between nodes

3. **Graph Type**:
   - `Schema__MGraph__Json__Graph`: Maintains the overall graph structure

#### Model Layer

The Model layer handles direct data manipulations and enforces type safety:

1. **Node Models**:
   - `Model__MGraph__Json__Node`: Base node operations
   - `Model__MGraph__Json__Node__Dict`: Dictionary operations
   - `Model__MGraph__Json__Node__List`: Array operations
   - `Model__MGraph__Json__Node__Value`: Value operations
   - `Model__MGraph__Json__Node__Property`: Property operations

2. **Graph Model**:
   - `Model__MGraph__Json__Graph`: Graph-wide operations and node type resolution

#### Domain Layer

The Domain layer implements high-level business logic and orchestrates operations:

1. **Node Domain Classes**:
   - `Domain__MGraph__Json__Node`: Base node functionality
   - `Domain__MGraph__Json__Node__Dict`: Dictionary manipulation
   - `Domain__MGraph__Json__Node__List`: Array manipulation
   - `Domain__MGraph__Json__Node__Value`: Value handling
   - `Domain__MGraph__Json__Node__Property`: Property management

2. **Graph Domain**:
   - `Domain__MGraph__Json__Graph`: High-level graph operations

## JSON Structure Representation

### Node Types and Their Roles

1. **Dict Nodes** (`Schema__MGraph__Json__Node__Dict`):
   - Represents JSON objects
   - Contains property-value pairs
   - Maintains property ordering

2. **List Nodes** (`Schema__MGraph__Json__Node__List`):
   - Represents JSON arrays
   - Maintains ordered sequence of values
   - Supports mixed type elements

3. **Value Nodes** (`Schema__MGraph__Json__Node__Value`):
   - Stores primitive JSON values
   - Handles: strings, numbers, booleans, null
   - Maintains type information

4. **Property Nodes** (`Schema__MGraph__Json__Node__Property`):
   - Represents object property names
   - Links to corresponding values
   - Stores property metadata

### Edge Relationships

The system uses edges to represent relationships between nodes:

1. **Object Properties**:
   ```
   Dict Node → Property Node → Value/Dict/List Node
   ```

2. **Array Elements**:
   ```
   List Node → Value/Dict/List Node
   ```

### JSON to Graph Mapping

The system transforms JSON structures into graph representations while preserving both structure and semantics. Here are key mapping patterns:

1. **Simple Object**
```json
{
    "name": "John",
    "age": 30
}
```
Graph Structure:
```
Dict Node ──→ Property("name") ──→ Value("John")
          └──→ Property("age")  ──→ Value(30)
```

2. **Nested Object**
```json
{
    "user": {
        "address": {
            "city": "London"
        }
    }
}
```
Graph Structure:
```
Dict Node ──→ Property("user") ──→ Dict Node ──→ Property("address") ──→ Dict Node ──→ Property("city") ──→ Value("London")
```

3. **Array with Mixed Types**
```json
{
    "items": [
        {"id": 1},
        42,
        "text",
        [1, 2]
    ]
}
```
Graph Structure:
```
Dict Node ──→ Property("items") ──→ List Node ──→ Dict Node ──→ Property("id") ──→ Value(1)
                                            ├──→ Value(42)
                                            ├──→ Value("text")
                                            └──→ List Node ──→ Value(1)
                                                          └──→ Value(2)
```

### Type System

The JSON provider implements comprehensive type handling through the `Schema__MGraph__Json__Types` class:

#### Type Mapping Table

| JSON Type | Python Type | Graph Node Type | Description |
|-----------|-------------|-----------------|-------------|
| object | dict | Dict Node | Container for key-value pairs |
| array | list | List Node | Ordered collection of values |
| string | str | Value Node | Text values |
| number | int/float | Value Node | Numeric values |
| boolean | bool | Value Node | True/false values |
| null | None | Value Node | Null/empty values |

```python
class Schema__MGraph__Json__Types:
    edge_type: Type[Schema__MGraph__Json__Edge]
    edge_config_type: Type[Schema__MGraph__Edge__Config]
    graph_data_type: Type[Schema__MGraph__Graph__Data]
    node_type: Type[Schema__MGraph__Json__Node]
    node_data_type: Type[Schema__MGraph__Node__Data]
```

## Key Operations

### Dictionary Operations

The `Domain__MGraph__Json__Node__Dict` class provides dictionary manipulation:

```python
def properties(self) -> Dict[str, Any]            # Get all properties
def property(self, name: str) -> Optional[Any]    # Get single property
def add_property(self, name: str, value: Any)     # Add/update property
def update(self, properties: Dict[str, Any])      # Bulk update
def delete_property(self, name: str) -> bool      # Remove property
```

### List Operations

The `Domain__MGraph__Json__Node__List` class handles array operations:

```python
def items (self                  ) -> List[Any]     # Get all items
def add   (self, value: Any      )                   # Add single item
def extend(self, items: List[Any])                  # Add multiple items
def remove(self, value: Any      ) -> bool          # Remove item
def clear (self                  )                  # Remove all items
```

### Value Operations

The `Domain__MGraph__Json__Node__Value` class manages primitive values:

```python
class Domain__MGraph__Json__Node__Value:
    value: Any                                      # The stored value
    value_type: type                                # Value's type
    def is_primitive(self) -> bool                  # Check if JSON primitive
```

## Graph Management

### Root Node System

The graph maintains a root node that serves as the entry point:

```python
def root            (self           ) -> Domain__MGraph__Json__Node                 # Get/create root
def root_content    (self           ) -> Optional[Domain__MGraph__Json__Node]       # Get content
def set_root_content(self, data: Any) -> Domain__MGraph__Json__Node
```

### Node Creation

The system provides specialized methods for creating different node types:

```python
def new_dict_node (self, properties = None) -> Domain__MGraph__Json__Node__Dict
def new_list_node (self, items      = None) -> Domain__MGraph__Json__Node__List
def new_value_node(self, value      : Any ) -> Domain__MGraph__Json__Node__Value
```

## Implementation Patterns

### Type Safety

1. The implementation uses Python's type hints extensively
2. Each layer maintains its own type definitions
3. Type validation occurs at the Schema layer
4. Model layer enforces type safety during operations


### Edge Management

Edges maintain relationships with specific attributes:

```python
class Schema__MGraph__Json__Edge:
    edge_config: Schema__MGraph__Json__Edge__Config
    from_node_id: Random_Guid
    to_node_id: Random_Guid
```
## Conclusion

The MGraph__Json implementation provides a robust foundation for representing and manipulating JSON data in a graph structure. Its clear separation of concerns, type safety, and comprehensive operation set make it a reliable pattern for implementing other data format providers in the MGraph system.