# MGraph Query Technical Specification

## Introduction

MGraph Query transforms complex graph operations into simple, intuitive property access. It sits atop MGraph's sophisticated graph infrastructure while presenting a clean, straightforward interface that feels natural to use. This combination of power and simplicity makes it an ideal tool for working with graph-based data structures, whether you're dealing with RSS feeds, JSON documents, or other structured data.

### How It Works

MGraph Query leverages two powerful underlying systems:

1. **MGraph_Json's Graph Structure**
   - Every piece of data is a node (articles, properties, values)
   - Relationships are edges connecting nodes
   - Clean separation of schema, model, and domain layers
   ```python
   # Internal representation example
   {
       'nodes': {
           'n1': {'type': 'article', 'data': {...}},
           'n2': {'type': 'property', 'name': 'title'},
           'n3': {'type': 'value', 'data': 'My Article'}
       },
       'edges': {
           'e1': {'from': 'n1', 'to': 'n2'},
           'e2': {'from': 'n2', 'to': 'n3'}
       }
   }
   ```

2. **MGraph__Index's Performance Layer**
   - O(1) lookups for nodes by type
   - O(1) access to relationships
   - Efficient attribute-based search
   ```python
   # What happens during query.article.title
   node_id = index.nodes_by_type['article'][0]
   prop_id = index.nodes_to_outgoing_edges[node_id]['title']
   value_id = index.nodes_to_outgoing_edges[prop_id]['value']
   ```

## Core Design Principles

### 1. Immediate Graph Traversal
- Each query operation maps directly to graph traversal operations
- No deferred execution or query planning
- Results available immediately upon node/edge access
- Operations execute in real-time, not batched

### 2. Native Graph Operations  
- Navigation follows natural node-edge relationships
- Property access translates directly to edge traversal
- Preserves underlying graph semantics and structure
- Maintains graph-native mental model

### 3. Type Safety
- Runtime type validation on all operations
- Type-aware navigation and traversal
- Safe null handling through optional chaining
- Type consistency across transformations

### 4. Performance-First Design
- O(1) lookups via indexed properties
- Efficient path traversal algorithms
- Minimal memory overhead
- Index-aware navigation

### 5. Intuitive API
- Property-based access mirrors data structure
- Natural Python syntax
- No SQL-like abstractions
- Direct mapping to mental model

## Implementation

### Basic Navigation

Navigation in MGraph Query is designed to feel as natural as working with regular Python objects. When you access properties or traverse relationships, the system automatically handles the complexities of graph traversal, node resolution, and type conversion. This allows you to focus on what data you want rather than how to get it.

MGraph Query provides immediate traversal of the graph through property access:

```python
query = mgraph.query()

# Direct property traversal
title = query.article.title  # Immediate edge traversal
author = query.article.author.name  # Multi-step traversal

# Array access
recent = query.articles[-5:]  # Direct index lookup
tagged = query.articles.tagged['tech']  # Property-based lookup

# Optional chaining using Python's or operator
email = query.article.author.contact.email or None  
name = query.article.author.name or 'Anonymous'
```

### Filtering

Filtering in MGraph Query happens during graph traversal, not as a separate operation. As you navigate through nodes and edges, filters act as path selectors, immediately narrowing the traversal to only the relevant parts of the graph. This direct filtering approach maintains the graph-native paradigm while providing powerful data selection capabilities.

Filters apply immediately during traversal:

```python
# Direct property matching
active = query.articles.with_status('active')
recent = query.articles.after('2024-01-01')

# Compound filters through chaining
featured = query.articles.with_status('published').featured()

# Property-based filtering
tech_news = query.articles.in_category('tech').by_author('verified')
```

### Graph Operations

Graph operations expose the full power of the underlying graph structure through an intuitive interface. Whether finding paths between nodes, traversing relationships, or performing complex graph analysis, each operation maps directly to graph traversal patterns. The system optimizes these operations using efficient graph algorithms and index structures while maintaining immediate execution semantics.

Operations execute directly on the graph:

```python
# Immediate path traversal
paths = query.paths.from_(start_node).through(['follows', 'collaborates'])

# Direct relationship traversal
related = query.traverse.from_(article).via('similar_to').top(5)
```

### Performance Features

Performance in MGraph Query comes from its intelligent use of index structures and efficient graph traversal algorithms. Rather than relying on query planning or optimization, the system maintains indexes that enable immediate O(1) access to nodes and relationships. This approach provides high performance while preserving the simplicity of direct graph traversal.

Index utilization happens automatically:

```python
# O(1) lookups via indexed properties
article = query.articles.by_id('123')
recent = query.articles.by_date('2024-01-23')

# Efficient traversal using indexed relationships
followers = query.users.followed_by(user_id)
```

### Type Safety

Type safety in MGraph Query combines runtime validation with intuitive navigation patterns. The system performs type checking during graph traversal, ensuring data consistency while providing helpful conversion utilities. This approach catches type errors early while maintaining the flexibility needed for working with diverse data structures.

Runtime type checking ensures data consistency:

```python
# Type validation during traversal
items = query.array_data.as_list()
metrics = query.number_data.as_int()

# Safe navigation with defaults
name = query.article.author.name or 'Anonymous'
```

## Real-World Examples

The following examples demonstrate how MGraph Query's principles translate into practical applications. Each example shows how direct graph traversal, immediate execution, and intuitive property access combine to solve real-world problems while maintaining clean, maintainable code.

### Content Navigation
```python
# Direct graph traversal for content access
article = query.articles.latest
title = article.title
author = article.author.name
comments = article.comments.recent(5)
```

### Relationship Analysis
```python
# Immediate relationship traversal
similar = query.articles.similar_to(current)
collaborators = query.authors.collaborated_with(author_id)
```

### Analytics

Analytics in MGraph Query leverage the graph structure to provide immediate insights. Rather than building complex queries, you directly traverse to the metrics you need, with the index system ensuring efficient access to aggregated data.

```
# Direct metric access
views = query.articles.category('tech').views.total
engagement = query.articles.recent(30).engagement.average
```

## Implementation Guidelines

The implementation of MGraph Query focuses on four critical areas that enable its core principles: efficient index structures, robust type safety, optimized performance, and comprehensive monitoring. These guidelines ensure that the system maintains its graph-native approach while delivering reliable, high-performance operations.

### 1. Index Structure
- Maintain O(1) lookup tables for common properties
- Index relationships for efficient traversal
- Update indices immediately on graph changes

### 2. Type System
- Implement runtime type checking
- Provide type conversion utilities
- Maintain type consistency during traversal

### 3. Performance
- Use efficient graph algorithms
- Minimize memory allocation
- Leverage index structures

### 4. Monitoring
- Track traversal performance
- Monitor index utilization
- Collect usage metrics

## Next Steps

The future development of MGraph Query focuses on three key areas that enhance its capabilities while maintaining its graph-native principles. These improvements will expand functionality, optimize performance, and improve the developer experience without compromising the system's immediate execution model.

### 1. Index Optimization
- Improve lookup performance
- Optimize memory usage
- Enhance traversal efficiency

2. **Graph Operations**
- Add pattern matching
- Implement path analysis
- Support graph algorithms

3. **Developer Experience**
- Add debugging tools
- Improve error messages
- Create visualization tools