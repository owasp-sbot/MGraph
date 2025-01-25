# MGraph Index Technical Guide

## Introduction

This technical guide documents the MGraph Index system - a critical performance optimization layer for MGraph data structures. It provides implementation details, optimization strategies, and integration patterns for efficient graph operations.

## Background

MGraph's core architecture uses a simple but powerful graph structure where nodes and edges are stored in dictionaries within Schema__MGraph__Graph objects. This design decision keeps the core system clean and flexible. However, it creates a significant performance challenge: there's no built-in way to efficiently query or traverse the graph.

The example below demonstrates the performance problem of finding nodes by type without an index. This operation requires scanning every node in the graph, resulting in O(n) complexity:

```python
# Without index - O(n) operation
def find_nodes_by_type(graph, node_type):
    return [node for node in graph.nodes.values() 
            if node.node_type == node_type]
```

The MGraph Index system solves this by maintaining pre-computed mappings of common relationships and properties, turning O(n) operations into O(1) lookups.

## Architecture Design

### Core Components

The core components define the fundamental data structures that power the index system. The Schema__MGraph__Index__Data class maintains seven distinct indexes, each optimizing a specific type of lookup operation. Each index is a dictionary mapping identifiers to sets of related identifiers, enabling constant-time access to node relationships, types, and attributes.

```python
# Schema layer defines core data structures
class Schema__MGraph__Index__Data:
    nodes_to_outgoing_edges: Dict[Obj_Id, Set[Obj_Id          ]]  # Fast edge lookup
    nodes_to_incoming_edges: Dict[Obj_Id, Set[Obj_Id          ]]  # Reverse relationships
    edge_to_nodes          : Dict[Obj_Id, tuple[Obj_Id, Obj_Id]]  # Node connectivity
    nodes_by_type          : Dict[str   , Set[Obj_Id          ]]  # Type-based lookup
    edges_by_type          : Dict[str   , Set[Obj_Id          ]]  # Edge classification
    nodes_by_attribute     : Dict[str   , Dict[Any, Set[Obj_Id]]] # Attribute indexing
    edges_by_attribute     : Dict[str   , Dict[Any, Set[Obj_Id]]] # Edge properties

class Schema__MGraph__Index(Type_Safe):
    data: Schema__MGraph__Index__Data
```

### Index Types and Usage

Each index type serves a specific query pattern. Below we demonstrate the three main index types: relationship indexes for edge traversal, type indexes for finding nodes/edges of specific types, and attribute indexes for property-based lookups. Each operation is O(1) as it involves a simple dictionary lookup rather than graph traversal.

#### Relationship Indexes

Relationship indexes provide instant access to the outgoing and incoming edges of any node and the connected nodes of any edge. They enable efficient graph traversal without requiring iteration over all nodes or edges.

```python
# O(1) edge lookup
outgoing = index.data.nodes_to_outgoing_edges[node_id]
incoming = index.data.nodes_to_incoming_edges[node_id]
from_node, to_node = index.data.edge_to_nodes[edge_id]
```

#### Type Indexes

Type indexes allow rapid filtering of nodes or edges by their type. These indexes are particularly useful in applications where specific graph components must be isolated for further processing.

```python
# Instant type-based access
value_nodes = index.data.nodes_by_type['Schema__MGraph__Json__Node__Value']
json_edges = index.data.edges_by_type['Schema__MGraph__Json__Edge']
```

#### Attribute Indexes

Attribute indexes facilitate efficient lookups based on the properties of nodes or edges. These indexes are crucial for property-based queries in large graphs.

```python
# Quick attribute lookup
high_priority = index.data.nodes_by_attribute['priority']['high']
modified_today = index.data.nodes_by_attribute['modified_date'][today]
```

## Implementation Guidelines

### 1. Index Building

The add_node method demonstrates the core indexing process. For each node, we maintain three types of indexes: edge relationships (both incoming and outgoing), type classification, and attribute mappings. The code carefully handles the initialization of nested data structures to ensure clean updates and prevent KeyError exceptions.

```python
class MGraph__Index(Type_Safe):
    def add_node(self, node: Schema__MGraph__Node) -> None:
        """Add node to all relevant indexes"""
        node_id = node.node_id
        node_type = node.node_type.__name__
        
        # Initialize edge maps
        if node_id not in self.data.nodes_to_outgoing_edges:
            self.data.nodes_to_outgoing_edges[node_id] = set()
        if node_id not in self.data.nodes_to_incoming_edges:
            self.data.nodes_to_incoming_edges[node_id] = set()
            
        # Add to type index
        if node_type not in self.data.nodes_by_type:
            self.data.nodes_by_type[node_type] = set()
        self.data.nodes_by_type[node_type].add(node_id)
        
        # Index attributes
        if hasattr(node, 'attributes') and node.attributes:
            self._index_attributes(node)
```

### 2. Persistence Support

The persistence implementation leverages Type_Safe's built-in JSON serialization capabilities. This provides a clean and efficient way to save and load index states. The save_to_file method serializes the entire index structure to JSON format, while load_from_file reconstructs the index from the saved data. Type_Safe handles all the complex serialization logic, including proper handling of sets and custom types.

```python
# Save index to file
def save_to_file(self, filename: str) -> None:
    """Save index state to file"""
    with open(filename, 'w') as f:
        f.write(self.json())

@classmethod
def load_from_file(cls, graph: Schema__MGraph__Graph, filename: str) -> 'MGraph__Index':
    """Load index from file"""
    with open(filename, 'r') as f:
        data = f.read()
    return cls.from_json(data)
```

### 3. Advanced Usage Patterns

The find_nodes_by_criteria method demonstrates how to combine multiple indexes for complex queries. It starts with a type-based lookup and then progressively refines the result set by intersecting it with attribute matches. This approach maintains high performance by leveraging set operations on the pre-computed indexes.

```python
def find_nodes_by_criteria(self, node_type: Type[Schema__MGraph__Node], 
                          attributes: Dict[str, Any]) -> Set[Obj_Id]:
    """Efficient multi-criteria search"""
    # Start with type-based set
    result = self.get_nodes_by_type(node_type)
    
    # Intersect with attribute matches
    for attr_name, attr_value in attributes.items():
        matching = self.get_nodes_by_attribute(attr_name, attr_value)
        result &= matching
    
    return result
```

#### Graph Analysis

Graph analysis tools are essential for understanding node connectivity and relationships. The following example demonstrates a method to analyze node connectivity, including outgoing, incoming, and bidirectional connections:

```python
def analyze_node_connectivity(self, node: Schema__MGraph__Node) -> Dict[str, int]:
    """Analyze node relationships"""
    node_id = node.node_id
    outgoing = self.get_node_outgoing_edges(node)
    incoming = self.get_node_incoming_edges(node)
    
    return {
        'outgoing_count': len(outgoing),
        'incoming_count': len(incoming),
        'total_connections': len(outgoing | incoming),
        'bidirectional': len(outgoing & incoming)
    }
```

## Integration Examples

The integration examples show how to combine the index system with existing MGraph components. The MGraph_Json_With_Index class demonstrates extending JSON functionality with indexed lookups, while the RSS provider example shows how to use the index for domain-specific queries like finding articles by date.

```python
class MGraph_Json_With_Index:
    def __init__(self):
        self.graph = Schema__MGraph__Graph()
        self.index = MGraph__Index(graph=self.graph)
    
    def find_value_nodes(self, value_type: type) -> Set[Obj_Id]:
        """Find nodes by value type"""
        value_nodes = self.index.get_nodes_by_type(Schema__MGraph__Json__Node__Value)
        return {node_id for node_id in value_nodes 
                if self.graph.nodes[node_id].value_type == value_type}
```

### With RSS Provider

The following example demonstrates how the index can be used for domain-specific queries, such as finding articles by publication date:

```python
class MGraph_RSS_With_Index:
    def find_articles_by_date(self, date: datetime) -> List[RSS_Item]:
        """Find articles by publication date"""
        # Use index for efficient lookup
        matching_nodes = self.index.get_nodes_by_attribute('pub_date', date)
        return [RSS_Item(self.graph.nodes[node_id]) for node_id in matching_nodes]
```

## Performance Benchmarks

The benchmark code provides a systematic way to measure the performance impact of indexing. It captures both the one-time cost of building the index and the ongoing benefits of fast lookups. The results typically show that while index building has an O(n) cost, the subsequent queries are consistently O(1) regardless of graph size.

```python
def benchmark_index_operations(graph_size: int = 10000):
    """Benchmark index performance"""
    results = {}
    
    # Build time
    start = time.time()
    index = MGraph__Index(graph)
    results['build_time'] = time.time() - start
    
    # Lookup operations
    start = time.time()
    for _ in range(1000):
        index.get_nodes_by_type(Schema__MGraph__Node)
    results['type_lookup'] = (time.time() - start) / 1000
    
    return results
```

## Conclusion

The MGraph Index system provides efficient querying and traversal capabilities while maintaining MGraph's clean core architecture. The one-time cost of index building and additional memory usage is offset by the dramatic performance improvements in query operations.

