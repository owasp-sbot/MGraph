# MGraph-DB: A Memory-based GraphDB for Python, GenAI, Semantic Web and Serverless

![Current Release](https://img.shields.io/badge/release-v1.1.0-blue)

MGraph-DB is a high-performance, type-safe graph database implementation in Python, optimized for in-memory operations with JSON persistence. Its architecture makes it particularly well-suited for:

- **GenAI Applications**
  - Knowledge graph construction and querying
  - Semantic relationship modeling
  - Context management for LLMs
  - Graph-based reasoning systems

- **Semantic Web**
  - RDF data processing
  - Ontology management
  - Linked data applications
  - SPARQL-compatible queries

- **Serverless Deployments**
  - Quick cold starts with memory-first design
  - Efficient JSON serialization
  - Low memory footprint
  - Built-in serverless support via [MGraph_DB_Serverless](https://github.com/owasp-sbot/MGraph-DB-Serverless)

- **Python Ecosystem**
  - Native Python implementation
  - Full type safety and validation
  - Clean, Pythonic API
  - Rich integration capabilities

## Major Features

### Production-Ready Type System
- Complete implementation of the three-layer architecture (Domain, Model, Schema)
- Comprehensive runtime type checking across all layers
- Type-safe property accessors and method decorators
- Robust validation for nested data structures
- Clean class hierarchies with explicit interfaces

### Advanced Graph Operations
- High-performance in-memory graph operations
- Sophisticated query system with chainable operations
- Rich traversal capabilities with type filtering
- Flexible node and edge attribute management
- Comprehensive CRUD operations for graph elements

### Optimized Indexing System
- O(1) lookups for all core operations
- Multi-dimensional indexing (type, attribute, relationship)
- Efficient graph traversal support
- Advanced query optimization
- Index persistence and restoration

### Query System Enhancements
- View-based query results with navigation
- Rich filtering and traversal operations
- Chainable query interface
- Query result caching
- Query operation history tracking

### Export Capabilities
- Support for multiple export formats:
  - GraphML
  - DOT
  - Mermaid
  - RDF/Turtle
  - N-Triples
  - GEXF
  - TGF
  - Cypher
  - CSV
  - JSON

### Visualization Support
- Integration with common visualization libraries
- Custom layout algorithms
- Interactive graph exploration
- Support for large graph visualization
- Multiple visualization format exports

## Quick Start

```python
from mgraph_db.mgraph.actions.MGraph__Data import MGraph__Data
from mgraph_db.mgraph.actions.MGraph__Edit import MGraph__Edit

# Create graph and get edit interface
edit = MGraph__Edit()
graph = edit.graph

# Add nodes
node_1 = edit.new_node(node_data={"value": "First Node" })
node_2 = edit.new_node(node_data={"value": "Second Node"})

# Create edge between nodes
edge = edit.new_edge(from_node_id = node_1.node_id,
                     to_node_id   = node_2.node_id)

# Query the graph
data = MGraph__Data(graph=graph)
nodes = data.nodes()        # Get all nodes
edges = data.edges()        # Get all edges
```

## Use Cases

### GenAI Integration
```python
from mgraph_db.mgraph.actions.MGraph__Edit import MGraph__Edit

# Create a knowledge graph for LLM context
edit = MGraph__Edit()
context  = edit.new_node(node_data    = {"type": "context", "value": "user query"  })
entity   = edit.new_node(node_data    = {"type": "entity" , "value": "named entity"})
relation = edit.new_edge(from_node_id = context.node_id     ,
                         to_node_id   = entity.node_id      ,
                         edge_data    = {"type": "contains"})
```

### Semantic Web Applications
```python
# RDF-style triples using MGraph
subject   = edit.new_node(node_data={"uri": "http://example.org/subject"})
object    = edit.new_node(node_data={"uri": "http://example.org/object"})
predicate = edit.new_edge(from_node_id = subject.node_id             ,
                          to_node_id   = object.node_id              ,
                          edge_data    = {"predicate": "relates_to"  })
```

## Advanced Usage

### Type-Safe Operations

```python
from mgraph_db.mgraph.schemas.Schema__MGraph__Node       import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data import Schema__MGraph__Node__Data

# Custom node data with runtime type checking
class Custom_Node_Data(Schema__MGraph__Node__Data):
    name: str                                                                   # Runtime type checking
    value: int                                                                  # for all fields
    priority: float

# Type-safe node definition
class Custom_Node(Schema__MGraph__Node):
    node_data: Custom_Node_Data                                                 # Ensures data integrity

# All operations are type-safe
def process_node(node: Custom_Node) -> float:                                  # Runtime type validation
    return node.node_data.priority * 2.0                                       # Type-safe access
```

### Using the Index System

```python
from mgraph_db.mgraph.actions.MGraph__Index import MGraph__Index

# Create index
index = MGraph__Index.from_graph(graph)

# Efficient lookups
nodes_by_type  = index.get_nodes_by_type(Custom_Node    )
nodes_by_field = index.get_nodes_by_field('name', 'test')
```

## Installation

```bash
pip install mgraph-db
```

## Development

```bash
# Clone repository
git clone https://github.com/your-org/mgraph-db.git

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.