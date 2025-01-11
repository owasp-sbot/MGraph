# MGraph Architecture Documentation

## Design Philosophy

MGraph implements a strict layered architecture with unidirectional dependencies. The architecture is organized into three core layers with additional supporting patterns for actions and persistence:

```
User Interface Layer
    ↓
Actions Layer
    ↓
Model Layer
    ↓
Schema Layer
```

## Core Layers

### 1. Schema Layer
- Defines data structures and type definitions
- Has no dependencies on other layers
- Uses only primitive types and other schema classes
- Enforces type safety through static typing
- Example: `Schema__MGraph__Node`, `Schema__MGraph__Edge`

#### Configuration Objects
Schema objects are often paired with configuration objects that contain immutable properties:
```python
class Schema__MGraph__Node(Type_Safe):
    value: Any
    attributes: Dict[Random_Guid, Schema__MGraph__Attribute]
    node_config: Schema__MGraph__Node__Config
    node_type: Type['Schema__MGraph__Node']

class Schema__MGraph__Node__Config(Type_Safe):
    node_id: Random_Guid
    value_type: type
```

### 2. Model Layer
- Implements business logic and data manipulation
- Depends only on Schema layer
- Returns only Model objects
- Encapsulates Schema objects
- Handles validation and type conversion
- Example: `Model__MGraph__Node`, `Model__MGraph__Edge`

#### Type Safety and Validation
```python
class Model__MGraph__Node:
    data: Schema__MGraph__Node
    
    def set_value(self, value) -> 'Model__MGraph__Node':
        if self.data.node_config.value_type:
            if not isinstance(value, self.data.node_config.value_type):
                raise TypeError(f"Value must be of type {self.data.node_config.value_type}")
        self.data.value = value
        return self
```

### 3. Actions Layer
The Actions layer provides focused interfaces for different types of operations on the graph. Each action class is responsible for a specific category of operations:

#### Core Action Classes
- `MGraph__Data`: Read operations and queries
- `MGraph__Edit`: Modification operations
- `MGraph__Filter`: Search and filtering capabilities
- `MGraph__Storage`: Persistence operations

Each action class:
- Depends only on Model layer
- Returns Model objects wrapped in action-specific interfaces
- Provides focused, purpose-specific operations
- Maintains single responsibility principle

Example action class structure:

Example:
```python
class MGraph:
    def data(self) -> MGraph__Data:      # Query operations
    def edit(self) -> MGraph__Edit:      # Modification operations
    def filter(self) -> MGraph__Filter:  # Search operations
    def storage(self) -> MGraph__Storage # Persistence operations
```

## Key Design Patterns

### 1. Type Registration
MGraph uses explicit type registration to maintain type safety across layers:

```python
class Schema__MGraph__Default__Types(Type_Safe):
    node_type: Type[Schema__MGraph__Node]
    edge_type: Type[Schema__MGraph__Edge]
    node_config_type: Type[Schema__MGraph__Node__Config]
    edge_config_type: Type[Schema__MGraph__Edge__Config]

class Model__MGraph__Graph(Type_Safe):
    node_model_type: Type[Model__MGraph__Node]
    edge_model_type: Type[Model__MGraph__Edge]

class MGraph__Graph(Type_Safe):
    node_domain_type: Type[MGraph__Node]
    edge_domain_type: Type[MGraph__Edge]
```

### 2. Action Pattern
Operations are grouped into focused interfaces:

```python
class MGraph__Data:
    def node(self, node_id: Random_Guid) -> MGraph__Node
    def nodes(self) -> List[MGraph__Node]
    def edge(self, edge_id: Random_Guid) -> MGraph__Edge
    def edges(self) -> List[MGraph__Edge]

class MGraph__Edit:
    def new_node(self, **kwargs) -> MGraph__Node
    def new_edge(self, **kwargs) -> MGraph__Edge
    def delete_node(self, node_id: Random_Guid) -> bool
    def delete_edge(self, edge_id: Random_Guid) -> bool
```

### 3. Storage Abstraction
The storage layer provides persistence operations:
```python
class MGraph__Storage:
    def create(self) -> MGraph__Graph  # Create new graph
    def delete(self) -> bool           # Delete current graph
    def safe(self) -> bool            # Save current state
```

## Key Design Principles

### 1. Unidirectional Dependencies
- Lower layers must not know about higher layers
- Schema layer is self-contained
- Model layer only knows about Schema
- Domain layer only knows about Model
- Action classes only know about Domain core

### 2. Type Isolation
- Each layer only returns objects of its own level
- Schema → Schema objects
- Model → Model objects (never Schema objects)
- Domain → Domain objects (never Model or Schema objects)
- Higher layers encapsulate lower layer objects

### 3. Clear Boundaries
- Explicit interfaces between layers
- No leaking of implementation details
- Strong encapsulation within each layer
- Actions provide focused interfaces

## Implementation Guidelines

### 1. Schema Layer
- Define clear type constraints
- Use configuration objects for immutable properties
- Implement basic validation
- Keep serializable
- Use only primitive types and other schemas

### 2. Model Layer
- Implement business logic
- Validate all operations
- Handle type conversion
- Encapsulate schema objects
- Return only model types

### 3. Domain Layer
Core Objects:
- Implement high-level logic
- Handle complex operations
- Return domain types only
- Maintain type safety

Action Classes:
- Group related operations
- Provide focused interfaces
- Handle specific concerns
- Return domain types

### 4. Storage Layer
- Abstract persistence details
- Handle serialization
- Manage graph lifecycle
- Support different backends

## Error Handling

### 1. Schema Layer
- Type validation errors
- Constraint violations
- Serialization errors

### 2. Model Layer
- Business rule violations
- Data validation errors
- State transition errors

### 3. Domain Layer
Core:
- Operation errors
- Workflow errors
- Integration errors

Actions:
- Input validation errors
- Operation-specific errors
- Storage errors

## Testing Strategy

### 1. Schema Tests
- Type validation
- Constraint checking
- Serialization/deserialization

### 2. Model Tests
- Business logic
- Validation rules
- Type conversion

### 3. Action Tests
- Operation sequences
- Error conditions
- Edge cases
- Action composition
- State transitions
- Operation authorization

### 4. Storage Tests
- Persistence operations
- State management
- Backend integration

## Common Pitfalls

### 1. Breaking Layer Isolation
```python
# BAD: Domain using Schema
class MGraph__Node:
    def __init__(self, schema: Schema__MGraph__Node)

# GOOD: Domain using Model
class MGraph__Node:
    def __init__(self, node: Model__MGraph__Node)
```

### 2. Mixing Action Responsibilities
```python
# BAD: Mixing concerns
class MGraph__Data:
    def delete_node(self)  # Should be in Edit

# GOOD: Focused interface
class MGraph__Data:
    def get_node(self)     # Query only
```

### 3. Exposing Implementation
```python
# BAD: Leaking schema
class Model__MGraph__Node:
    def get_raw_data(self) -> Schema__MGraph__Node

# GOOD: Clean interface
class Model__MGraph__Node:
    def get_value(self) -> Any
```

## Best Practices

### 1. Naming Conventions
- Schema classes: `Schema__*`
- Model classes: `Model__*`
- Domain classes: `MGraph__*`
- Action classes: `MGraph__*_{Action}`

### 2. Type Safety
- Use type hints consistently
- Validate at boundaries
- Register types explicitly
- Document constraints

### 3. Error Handling
- Use specific exceptions
- Handle errors at appropriate layer
- Maintain error context
- Provide clear messages

### 4. Documentation
- Document public interfaces
- Specify type contracts
- Explain validation rules
- Provide examples

## Migration Path

When adding features:

1. Schema Layer
   - Add data structures
   - Define constraints
   - Update type registry

2. Model Layer
   - Implement logic
   - Add validation
   - Update type registry

3. Domain Layer
   - Add domain logic
   - Create action classes
   - Update interfaces

4. Storage Layer
   - Update persistence
   - Handle migration
   - Update backends

## Conclusion

This architecture provides a robust foundation for building maintainable and scalable graph-based applications. The combination of strict layering, action classes, and clear type safety makes it easy to understand, test, and extend the system while maintaining code quality.