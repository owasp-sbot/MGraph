# MGraph__Json Class Technical Specification

_Document created: January 15, 2025_

## Overview

MGraph__Json provides the primary interface for working with JSON documents in the MGraph system. It converts JSON data structures into graph representations while preserving their semantic meaning and relationships, allowing powerful graph operations on JSON data.

This class serves as the main entry point for developers working with JSON in MGraph, handling document import, manipulation, and export while abstracting the complexities of the underlying graph representation.

## Related Documentation

Understanding MGraph__Json requires familiarity with several interconnected components of the MGraph system. Each related document provides essential context for different aspects of JSON handling in MGraph:

- **MGraph Architecture Analysis**: Defines the core graph system architecture and operational layers that MGraph__Json builds upon. This foundation determines how JSON structures map to graph elements.
- **MGraph Core Schema**: Details the foundational graph data structures and relationships that enable JSON representation. The schema ensures consistent and type-safe JSON handling.
- **MGraph JSON Root Node**: Specifies the root node system for JSON documents, which is crucial for maintaining valid JSON structure and enabling proper traversal.
- **MGraph Testing Best Practices**: Provides testing patterns relevant to JSON operations, ensuring reliability and consistency in JSON handling.

## Use Cases and Requirements

Before diving into implementation details, it's essential to understand why developers need MGraph__Json and what problems it solves. JSON handling in graph systems presents unique challenges that require careful consideration of structure preservation, relationship mapping, and semantic meaning.

Developers need to perform these key operations with JSON data:

1. Load JSON from various sources (files, APIs, strings) into a graph representation
2. Manipulate JSON structure and content using graph operations
3. Export modified JSON back to standard formats
4. Maintain JSON semantics and relationships during transformations
5. Handle complex JSON structures including nested objects and arrays

## JSON to Graph Mapping Examples

Understanding how JSON structures map to graph representations is fundamental to working with MGraph__Json. These examples demonstrate the transformation process for common JSON patterns, showing how the system preserves both structure and relationships in the graph representation. Each example illustrates a different aspect of JSON handling, from simple key-value pairs to complex nested structures.

### 1. Simple Key-Value Object
JSON Input:
```json
{
    "name": "John",
    "age": 30
}
```
Graph Structure:
```
ROOT ─→ DICT ─→ PROPERTY("name") ─→ VALUE("John")
              └─→ PROPERTY("age")  ─→ VALUE(30)
```

### 2. Nested Objects
JSON Input:
```json
{
    "user": {
        "details": {
            "address": {
                "city": "London"
            }
        }
    }
}
```
Graph Structure:
```
ROOT ─→ DICT ─→ PROPERTY("user") ─→ DICT ─→ PROPERTY("details") ─→ DICT ─→ PROPERTY("address") ─→ DICT ─→ PROPERTY("city") ─→ VALUE("London")
```

### 3. Arrays and Mixed Types
JSON Input:
```json
{
    "items": [
        {"id": 1, "value": "first"},
        {"id": 2, "value": "second"},
        42,
        "string",
        [1, 2, 3]
    ]
}
```
Graph Structure:
```
ROOT ─→ DICT ─→ PROPERTY("items") ─→ LIST ─→ DICT ─→ PROPERTY("id") ─→ VALUE(1)
                                             │       └─→ PROPERTY("value") ─→ VALUE("first")
                                             ├─→ DICT ─→ PROPERTY("id") ─→ VALUE(2)
                                             │       └─→ PROPERTY("value") ─→ VALUE("second")
                                             ├─→ VALUE(42)
                                             ├─→ VALUE("string")
                                             └─→ LIST ─→ VALUE(1)
                                                     ├─→ VALUE(2)
                                                     └─→ VALUE(3)
```

## Class Architecture

The architecture of MGraph__Json follows a clear separation of concerns, with distinct components handling different aspects of JSON processing. This design ensures maintainability, extensibility, and clear operational boundaries. Each component focuses on a specific aspect of JSON handling, from basic graph operations to specialized JSON-specific functionality.

### Main Interface

The main interface provides a clean, intuitive API for working with JSON documents. It follows the established MGraph patterns while adding JSON-specific capabilities. This consistent interface design makes the system immediately familiar to MGraph developers while providing powerful JSON handling features.

```python
class MGraph__Json:                                                                # Main JSON graph manager
    def __init__(self):                                                           # Initialize graph manager
        self.graph = Domain__MGraph__Json__Graph()                                  
        
    def data(self)    -> MGraph__Data:                                           # Access data operations
    def edit(self)    -> MGraph__Edit:                                           # Access edit operations
    def export(self)  -> MGraph__Json__Export:                                   # Access export operations
    def import_(self) -> MGraph__Json__Import:                                   # Access import operations
    def storage(self) -> MGraph__Storage:                                        # Access storage operations
```

### Import Operations

The import system handles the critical task of converting JSON from various sources into the graph representation. It provides multiple entry points to accommodate different input sources, making the system flexible and adaptable to various use cases. Each import method handles specific source types while maintaining consistent behavior and error handling.

```python
class MGraph__Json__Import:                                                      # JSON import operations
    def from_string(self, json_str: str    ) -> Domain__MGraph__Json__Graph:    # Import from JSON string
    def from_dict  (self, data: Any        ) -> Domain__MGraph__Json__Graph:    # Import from Python object
    def from_file  (self, file_path: str   ) -> Domain__MGraph__Json__Graph:    # Import from file
    def from_url   (self, url: str         ) -> Domain__MGraph__Json__Graph:    # Import from URL
```

### Export Operations

Export operations are responsible for converting the graph representation back into standard JSON formats. This system ensures that the graph structure can be accurately serialized while maintaining JSON semantics. The export process handles formatting, validation, and proper type conversion.

```python
class MGraph__Json__Export(MGraph__Export):                                      # JSON export operations
    def to_dict  (self                            ) -> Union[Dict, List, Any]:  # Export to Python object
    def to_string(self, indent: Optional[int] = None) -> str:                   # Export to JSON string
    def to_file  (self, file_path: str,                                         # Export to JSON file
                       indent: Optional[int] = None  ) -> bool:                   
```

## Detailed Operation Specifications

This section provides in-depth details about the internal processes that make JSON handling possible. Understanding these operations is crucial for both using the system effectively and maintaining or extending its functionality.

### Import Process Flow

The import process represents one of the most critical operations in MGraph__Json. It must handle various input formats, validate content, and create a correct graph representation while maintaining performance and memory efficiency. The three-phase approach ensures reliable and consistent JSON processing.

1. Input Processing handles the initial data acquisition:
   - Validates input format and accessibility
   - Parses JSON (for string inputs)
   - Handles character encoding
   - Manages streaming for large files

2. Graph Construction builds the internal representation:
   - Creates or updates the root node
   - Constructs the node hierarchy
   - Establishes proper relationships
   - Preserves JSON semantics

3. Error Handling manages failure cases:
   - Detects invalid JSON syntax
   - Handles file access issues
   - Manages network errors for URLs
   - Controls memory constraints

### Export Process Flow

The export process ensures proper JSON generation:

1. Graph Traversal extracts the structure:
   - Starts from the root node
   - Builds the object hierarchy
   - Maintains proper ordering
   - Handles circular references

2. Output Generation creates the final format:
   - Applies proper indentation
   - Handles special characters
   - Manages large documents
   - Validates output structure

### Type Handling

Type mapping between JSON and graph representations forms the foundation of accurate data handling. This system ensures that JSON types are correctly represented in the graph while maintaining the ability to round-trip data without loss of information or type fidelity.

| JSON Type | Python Type | Graph Node Type | Description                    |
|-----------|-------------|-----------------|--------------------------------|
| object    | dict        | Dict Node       | JSON object container         |
| array     | list        | List Node       | Ordered value collection      |
| string    | str         | Value Node      | Text values                   |
| number    | int/float   | Value Node      | Numeric values               |
| boolean   | bool        | Value Node      | True/false values            |
| null      | None        | Value Node      | Null/empty values            |

