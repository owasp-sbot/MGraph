# MGraph-AI - A Memory-based GraphDB for GenAI, Semantic Web and Serverless

![Current Release](https://img.shields.io/badge/release-v0.5.0-blue)

MGraph-AI is a lightweight, memory-first graph database implementation in Python, designed specifically for AI, semantic web, 
and serverless applications. What sets it apart is its focus on in-memory performance while maintaining persistence through 
serialized JSON data structures. This makes it particularly well-suited for:

- AI/ML applications requiring fast graph traversals
- Serverless environments where quick startup and low memory overhead are crucial
- Semantic web applications needing flexible graph structures
- Applications requiring both graph capabilities and JSON compatibility

The library provides a robust, type-safe implementation with a clean, layered architecture that prioritizes maintainability 
and scalability. By keeping the graph in memory and serializing to JSON, MGraph-AI achieves excellent performance from small to read-heavy 
workloads while maintaining data persistence.

## Features

- Memory-first architecture with JSON serialization for persistence
- High-performance graph operations optimized for in-memory access
- Type-safe implementation with comprehensive validation
- Clean, layered architecture with focused action interfaces
- Rich attribute support for nodes and edges
- Extensible storage backends with JSON as the primary format
- Minimal dependencies making it ideal for serverless deployments
- Built-in support for semantic web concepts
- Optimized for AI/ML workloads
- Small memory footprint with efficient serialization

## Installation

```bash
pip install mgraph-ai
```

## Quick Start

```python
from mgraph_ai.mgraph import MGraph
from osbot_utils.helpers.Safe_Id import Safe_Id

# Create a new graph
mgraph = MGraph()

# Add nodes and edges
with mgraph.edit() as edit:
    # Create nodes
    node1 = edit.new_node(value="Node 1")
    node2 = edit.new_node(value="Node 2")
    
    # Add attributes to nodes
    node1.add_attribute(name=Safe_Id("color"), value="blue")
    node2.add_attribute(name=Safe_Id("size"), value=5)
    
    # Create an edge between nodes
    edge = edit.new_edge(from_node_id=node1.node_id(), 
                        to_node_id=node2.node_id())
    
    # Add attribute to edge
    edge.add_attribute(name=Safe_Id("weight"), value=1.5)

# Query the graph
with mgraph.data() as data:
    # Get all nodes
    nodes = data.nodes()
    
    # Get all edges
    edges = data.edges()
    
    # Get specific node
    node = data.node(node1.node_id())
```

## Architecture

MGraph-AI implements a layered architecture:

```
Actions Layer (Data, Edit, Filter, Storage)
    ↓
Model Layer (Business Logic)
    ↓
Schema Layer (Type Definitions)
```

### Action Classes

Operations are organized into focused interfaces:

- `MGraph__Data`: Read operations and queries
- `MGraph__Edit`: Modification operations
- `MGraph__Filter`: Search and filtering capabilities
- `MGraph__Storage`: Persistence operations

### Type Safety

MGraph-AI enforces type safety at all layers:

```python
# Type-safe node creation
node = edit.new_node(value="test", value_type=str)  # OK
node = edit.new_node(value=123, value_type=str)     # Raises TypeError

# Type-safe attribute addition
node.add_attribute(name=Safe_Id("count"), 
                  value=42, 
                  attr_type=int)  # OK
```

## Advanced Usage

### Custom Node Types

```python
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node import Schema__MGraph__Node

class Custom_Node(Schema__MGraph__Node):
    def custom_method(self):
        return f"Node value: {self.value}"

# Use custom node type
mgraph = MGraph(node_type=Custom_Node)
```

### Graph Persistence

```python
# Save graph state
with mgraph.storage() as storage:
    storage.save()

# Create new graph
with mgraph.storage() as storage:
    storage.create()

# Delete graph
with mgraph.storage() as storage:
    storage.delete()
```

### Attribute Operations

```python
# Add typed attributes
node.add_attribute(name=Safe_Id("count"), value=42, attr_type=int)
node.add_attribute(name=Safe_Id("name"), value="test", attr_type=str)

# Get attribute value
attr = node.attribute(attribute_id)
value = attr.value()

# Get all attributes
attributes = node.attributes()
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/owasp-sbot/MGraph-AI.git
cd MGraph-AI

# Install dependencies with Poetry
poetry install

# Enter the poetry shell
poetry shell

# Run tests
poetry run pytest tests/
```

## License

This project is licensed under the Apache 2.0 License 2.0 - see the [LICENSE](LICENSE) file for details.
