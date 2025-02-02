# MGraph-DB Architecture Overview

## Introduction

MGraph-DB is a universal graph-based data transformation and manipulation system designed to provide a flexible foundation for representing and manipulating connected data structures. This document outlines its core architecture, components, and design principles.

## Architecture Overview

### Three-Layer Architecture

MGraph-DB implements a three-layer architecture that separates concerns and provides clear responsibilities:

#### 1. Schema Layer (Base Layer)
- **Purpose**: Defines pure data structures and validation rules
- **Responsibilities**:
  - Basic type definitions
  - Data structure validation
  - No business logic
  - Pure data containers
- **Key Components**:
```python
class Schema__MGraph__Node:
    node_data: Schema__MGraph__Node__Data
    node_type: Type['Schema__MGraph__Node']

class Schema__MGraph__Edge:
    from_node_id: Random_Guid
    to_node_id: Random_Guid
    edge_type: Type['Schema__MGraph__Edge']

class Schema__MGraph__Graph:
    nodes: Dict[Random_Guid, Schema__MGraph__Node]
    edges: Dict[Random_Guid, Schema__MGraph__Edge]
    graph_data: Schema__MGraph__Graph__Data
```

#### 2. Model Layer (Middle Layer)
- **Purpose**: Handles direct data manipulations
- **Responsibilities**:
  - Data integrity maintenance
  - Type safety enforcement
  - Basic operations
  - Single model/schema interactions
- **Key Components**:
```python
class Model__MGraph__Node:
    data: Schema__MGraph__Node
    
class Model__MGraph__Edge:
    data: Schema__MGraph__Edge
    
class Model__MGraph__Graph:
    data: Schema__MGraph__Graph
    model_types: Model__MGraph__Types
```

#### 3. Domain Layer (Top Layer)
- **Purpose**: Implements business logic and orchestrates operations
- **Responsibilities**:
  - Cross-entity operations
  - Business rule implementation
  - High-level functionality
  - Graph-wide consistency
- **Key Components**:
```python
class Domain__MGraph__Node:
    node: Model__MGraph__Node
    graph: Model__MGraph__Graph
    
class Domain__MGraph__Edge:
    edge: Model__MGraph__Edge
    graph: Model__MGraph__Graph
```

## Core Design Principles

### 1. Minimal Core Structure
The system is built on three fundamental principles:
- Nodes exist
- Edges connect nodes
- Everything else is implementation-specific

### 2. Type System
Each layer maintains its own type definitions:
```python
class Schema__MGraph__Types:
    node_type: Type[Schema__MGraph__Node]
    edge_type: Type[Schema__MGraph__Edge]
    
class Model__MGraph__Types:
    node_model_type: Type[Model__MGraph__Node]
    edge_model_type: Type[Model__MGraph__Edge]
    
class Domain__MGraph__Types:
    node_domain_type: Type[Domain__MGraph__Node]
    edge_domain_type: Type[Domain__MGraph__Edge]
```

### 3. Identity Management
- Uses GUIDs for unique identification
- Manages identities through dictionary keys
- Separates identity concerns from schema layer

## Features and Capabilities

### 1. Context Manager Support
```python
with graph.edit() as edit:
    # Create new nodes and edges
    node = edit.new_node()
    edge = edit.new_edge(from_node_id=node1.id, to_node_id=node2.id)
```

### 2. Static Graph Templates
Provides built-in graph patterns:
```python
class MGraph__Static__Graph:
    def linear_graph(self, num_nodes: int = 3)
    def circular_graph(self, num_nodes: int = 3)
    def star_graph(self, num_spokes: int = 3)
    def complete_graph(self, num_nodes: int = 3)
```

### 3. Multi-Format Support
Supports multiple data formats:
- JSON
- XML/RSS
- RDF/Turtle
- CSV
- GraphML
- Neo4j Cypher
- N-Triples
- GEXF
- TGF

### 4. Provider System
Allows format-specific implementations:
```python
class Provider_Specific_Node(Schema__MGraph__Node):
    def __init__(self):
        self.format_specific = {}  # Custom data structure
```

## Data Flow Architecture

### Provider Data Flow
1. **Input Phase**
   - External data parsing
   - Format-specific validation
   - Conversion to internal format

2. **Processing Phase**
   - Graph manipulation
   - Data transformation
   - Query operations

3. **Output Phase**
   - Format-specific serialization
   - Data validation
   - Output optimization

## Implementation Guidelines

### 1. Provider Implementation
When implementing new providers:
- Extend base schema classes
- Define format-specific data structures
- Implement serialization methods
- Handle format-specific validation

### 2. Graph Operations
Basic operations include:
- Node creation/deletion
- Edge creation/deletion
- Graph traversal
- Data manipulation

### 3. Type Safety
- Use type hints consistently
- Implement validation at schema layer
- Maintain type safety across layers
- Handle type conversions appropriately

## Best Practices

1. **Use Context Managers**
   - Always use with graph editing
   - Ensures proper state management
   - Maintains data consistency

2. **Layer Separation**
   - Keep schema layer pure
   - Handle business logic in domain layer
   - Maintain clear layer boundaries

3. **Error Handling**
   - Validate inputs at appropriate layers
   - Provide clear error messages
   - Handle edge cases gracefully

## Conclusion

MGraph-DB's architecture provides a robust foundation for graph-based data management while maintaining flexibility and extensibility. Its layered approach and minimal core structure allow for diverse implementations while ensuring consistency and reliability.
