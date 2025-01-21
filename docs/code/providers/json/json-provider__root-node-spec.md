# MGraph JSON Root Node Technical Specification

## Overview

The MGraph JSON implementation provides a graph-based representation of JSON documents, enabling powerful manipulation and transformation capabilities. This specification focuses on the root node system, which serves as the foundation for ensuring valid JSON document structure and maintaining consistency during operations.

The root node concept is critical because every valid JSON document must have exactly one root element (whether it's an object, array, or value). Our graph representation enforces this through a specialized root node design.

## Core Concepts

This section outlines the fundamental design decisions and structures that enable proper JSON document representation in a graph format. Understanding these concepts is essential for implementing and working with JSON documents in MGraph.

### Root Node Design
- Root node is a simple `Domain__MGraph__Json__Node` without specialization
- Acts as a container/anchor point for the actual JSON content
- Only one root node per JSON graph
- Stored in `graph_data.root_id`
- Created automatically on first access

For example, this JSON:
```json
"hello world"
```
Is represented as:
```
ROOT ─→ VALUE("hello world")
```

And this JSON:
```json
{
  "greeting": "hello world"
}
```
Is represented as:
```
ROOT ─→ DICT ─→ PROPERTY("greeting") ─→ VALUE("hello world")
```

### Node Types Hierarchy

The node hierarchy reflects the different types of elements that can exist in a JSON document. This structure ensures that we can represent any valid JSON while maintaining proper relationships between elements.

#### Root Node (`Domain__MGraph__Json__Node`)
- Base node type
- No special data/properties
- Only one per graph
- Always parent, never child

Example:
```json
42  // Single value JSON document
```
Graph structure:
```
ROOT ─→ VALUE(42)
```

#### Content Node Types

1. Value Node (`Domain__MGraph__Json__Node__Value`)
   - Holds primitive JSON values (string, number, boolean, null)
   - Always leaf node (no children)
   
   Examples:
   ```json
   "string value"
   42
   true
   null
   ```
   
2. List Node (`Domain__MGraph__Json__Node__List`)
   - Represents JSON arrays
   - Can contain multiple children
   
   Example:
   ```json
   [1, "two", true, {"key": "value"}]
   ```
   Graph structure:
   ```
   ROOT ─→ LIST ─→ VALUE(1)
                 ├─→ VALUE("two")
                 ├─→ VALUE(true)
                 └─→ DICT ─→ PROPERTY("key") ─→ VALUE("value")
   ```
   
3. Dictionary Node (`Domain__MGraph__Json__Node__Dict`)
   - Represents JSON objects
   - Contains property nodes as children
   
   Example:
   ```json
   {
     "name": "John",
     "age": 30,
     "address": {
       "city": "New York"
     }
   }
   ```
   Graph structure:
   ```
   ROOT ─→ DICT ─→ PROPERTY("name") ─→ VALUE("John")
                 ├─→ PROPERTY("age") ─→ VALUE(30)
                 └─→ PROPERTY("address") ─→ DICT ─→ PROPERTY("city") ─→ VALUE("New York")
   ```
   
4. Property Node (`Domain__MGraph__Json__Node__Property`)
   - Represents object property names
   - Must have exactly one parent (Dict) and one child

## Connection Rules

This section defines the allowed relationships between different node types. These rules are crucial for maintaining valid JSON structure and preventing invalid graph states that couldn't be serialized back to JSON.

### Valid Parent-Child Relationships

```
ROOT NODE
├── can parent: DICT, LIST, VALUE
└── can be parented by: nothing

DICT NODE
├── can parent: PROPERTY only
└── can be parented by: ROOT, LIST, PROPERTY

LIST NODE
├── can parent: DICT, LIST, VALUE
└── can be parented by: ROOT, LIST, PROPERTY

PROPERTY NODE
├── can parent: DICT, LIST, VALUE
└── can be parented by: DICT only

VALUE NODE
├── can parent: nothing
└── can be parented by: ROOT, LIST, PROPERTY
```

Examples of valid JSON and their graph structures:

1. Simple object:
```json
{
  "key": "value"
}
```
```
ROOT ─→ DICT ─→ PROPERTY("key") ─→ VALUE("value")
```

2. Nested array:
```json
[1, [2, 3], 4]
```
```
ROOT ─→ LIST ─→ VALUE(1)
              ├─→ LIST ─→ VALUE(2)
              │          └─→ VALUE(3)
              └─→ VALUE(4)
```

3. Complex nesting:
```json
{
  "items": [
    {"id": 1},
    {"id": 2}
  ],
  "total": 2
}
```
```
ROOT ─→ DICT ─→ PROPERTY("items") ─→ LIST ─→ DICT ─→ PROPERTY("id") ─→ VALUE(1)
                                          └─→ DICT ─→ PROPERTY("id") ─→ VALUE(2)
              └─→ PROPERTY("total") ─→ VALUE(2)
```

### Edge Constraints

1. Root Node Edges
   - Maximum of one outgoing edge
   - No incoming edges allowed
   - Must point to a content node

Example:
```json
{"valid": true}
```
Valid graph:
```
ROOT ─→ DICT ─→ PROPERTY("valid") ─→ VALUE(true)
```

2. Property Node Edges
   - Exactly one incoming edge (from Dict)
   - Exactly one outgoing edge (to content)

Example:
```json
{
  "user": {
    "name": "John"
  }
}
```
```
ROOT ─→ DICT ─→ PROPERTY("user") ─→ DICT ─→ PROPERTY("name") ─→ VALUE("John")
```

3. Value Node Edges
   - Maximum of one incoming edge
   - No outgoing edges allowed

Example:
```json
[42, 42]  // Same value can appear multiple times
```
```
ROOT ─→ LIST ─→ VALUE(42)
              └─→ VALUE(42)  // Separate node instance
```

4. List Node Edges
   - One incoming edge
   - Multiple outgoing edges allowed

Example:
```json
[1, 2, [3, 4]]
```
```
ROOT ─→ LIST ─→ VALUE(1)
              ├─→ VALUE(2)
              └─→ LIST ─→ VALUE(3)
                        └─→ VALUE(4)
```

5. Dict Node Edges
   - One incoming edge
   - Multiple outgoing edges allowed
   - All children must be Property nodes

Example:
```json
{
  "a": 1,
  "b": {"c": 2}
}
```
```
ROOT ─→ DICT ─→ PROPERTY("a") ─→ VALUE(1)
              └─→ PROPERTY("b") ─→ DICT ─→ PROPERTY("c") ─→ VALUE(2)
```

## Implementation Requirements

This section covers the technical requirements for implementing the root node system. These requirements ensure proper graph construction, validation, and maintenance.

### Root Management

```python
class Domain__MGraph__Json__Graph:
    def root(self) -> Domain__MGraph__Json__Node:
        """Get or create root node"""
        
    def root_content(self) -> Optional[Domain__MGraph__Json__Node]:
        """Get typed content node"""
        
    def set_root_content(self, data: Any) -> Domain__MGraph__Json__Node:
        """Set/replace root content"""
```

Example usage with different JSON types:
```python
# String value
graph.set_root_content("hello")  # "hello"

# Number value
graph.set_root_content(42)       # 42

# Array
graph.set_root_content([1,2,3])  # [1, 2, 3]

# Object
graph.set_root_content({         # {"name": "John"}
    "name": "John"
})
```

### Validation Requirements

1. Node Creation
   - Validate parent-child relationships
   - Enforce single root constraint
   - Check edge constraints

Example of invalid JSON structure that should be prevented:
```python
# Invalid: Multiple roots
graph.set_root_content("first")
graph.set_root_content("second")  # Should replace, not add second root

# Invalid: Property node at root
graph.set_root_content(Property("key"))  # Properties must be children of Dict
```

2. Edge Creation
   - Verify allowed connections
   - Maintain parent-child rules
   - Check node type compatibility

Example of invalid connections:
```python
# Invalid: Value node can't have children
value_node.add_child(another_node)

# Invalid: Property not under Dict
list_node.add_child(property_node)
```

3. Content Management
   - Clean up old content on replacement
   - Maintain valid graph state
   - Handle type transitions

Example of valid content replacement:
```python
# Replace string with array
graph.set_root_content("old")
graph.set_root_content(["new"])

# Replace array with object
graph.set_root_content(["old"])
graph.set_root_content({"new": true})
```

## Valid JSON Document Representations

This section demonstrates how different JSON structures are represented in the graph. Understanding these patterns is essential for working with the graph representation.

### 1. Single Value
JSON:
```json
"hello world"
```
Graph:
```
ROOT ─→ VALUE("hello world")
```

### 2. Array
JSON:
```json
[
  "item1",
  "item2",
  {"key": "value"}
]
```
Graph:
```
ROOT ─→ LIST ─→ VALUE("item1")
              ├─→ VALUE("item2")
              └─→ DICT ─→ PROPERTY("key") ─→ VALUE("value")
```

### 3. Object
JSON:
```json
{
  "key1": "value1",
  "key2": ["item"],
  "key3": {
    "nested": true
  }
}
```
Graph:
```
ROOT ─→ DICT ─→ PROPERTY("key1") ─→ VALUE("value1")
              ├─→ PROPERTY("key2") ─→ LIST ─→ VALUE("item")
              └─→ PROPERTY("key3") ─→ DICT ─→ PROPERTY("nested") ─→ VALUE(true)
```

## Edge Cases & Error Handling

This section covers special situations and error conditions that must be handled properly to maintain graph integrity.

1. Empty Graph
   ```python
   graph = Domain__MGraph__Json__Graph()
   root = graph.root()  # Creates root
   assert graph.root_content() is None  # No content yet
   ```

2. Content Replacement
   ```python
   # Replace primitive with object
   graph.set_root_content(42)
   graph.set_root_content({"value": 42})
   
   # Replace object with array
   graph.set_root_content({"key": "value"})
   graph.set_root_content(["value"])
   ```

3. Invalid Operations
   ```python
   # Invalid: Create second root
   root1 = graph.root()
   root2 = graph.new_root()  # Should raise error
   
   # Invalid: Connect value to value
   value1 = graph.new_value_node(1)
   value2 = graph.new_value_node(2)
   graph.new_edge(value1, value2)  # Should raise error
   ```

## Example Usage

This section provides practical examples of working with the root node system, demonstrating common patterns and best practices.

```python
# Create empty graph
graph = Domain__MGraph__Json__Graph()

# Get root (creates if needed)
root = graph.root()
assert graph.root_content() is None  # No content yet

# Set string value
content = graph.set_root_content("test")
assert isinstance(content, Domain__MGraph__Json__Node__Value)

# Complex object example
content = graph.set_root_content({
    "id": 1,
    "tags": ["a", "b"],
    "metadata": {
        "created": "2024-01-15",
        "active": true
    }
})
```

## Best Practices

This section provides guidelines for working effectively with the root node system while maintaining code quality and graph integrity.

1. Always access root through `root()` method:
   ```python
   # Good
   root = graph.root()
   
   # Bad
   root = graph.model.data.graph_data.root_id  # Direct access
   ```

2. Use `root_content()` to get typed content node:
   ```python
   # Good
   content = graph.root_content()
   if isinstance(content, Domain__MGraph__Json__Node__Dict):
       # Handle dict case
   
   # Bad
   root = graph.root()
   edges = graph.model.node__from_edges(root.node_id)  # Manual traversal
   ```

3. Use `set_root_content()` for content changes:
   ```python
   # Good
   graph.set_root_content({"new": "content"})
   
   # Bad
   root = graph.root()
   dict_node = graph.new_dict_node()
   graph.new_edge(root.node_id, dict_node.node_id)  # Manual edge creation
   ```

4. Follow JSON specification for valid document types:
   ```python
   # Valid JSON roots
   graph.set_root_content("string")
   graph.set_root_content(42)
   graph.set_root_content(True)
   graph.set_root_content(None)
   graph.set_root_content(["array"])
   graph.set_root_content({"object": true})
   
   # Invalid JSON roots
   graph.set_root_content(complex(1,2))  # Complex numbers not in JSON
   graph.set_root_content(set([1,2,3]))  # Sets not in JSON
   ```
