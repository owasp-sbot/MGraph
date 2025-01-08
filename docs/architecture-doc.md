# MGraph Architecture Documentation

## Design Philosophy

MGraph implements a strict layered architecture with unidirectional dependencies:

```
Domain Layer (Top)
    ↓
Model Layer
    ↓
Schema Layer (Bottom)
```

### Layer Responsibilities

#### 1. Schema Layer
- Defines data structures and type definitions
- Has no dependencies on other layers
- Uses only primitive types and other schema classes
- Enforces type safety through static typing
- Example: `Schema__MGraph__Node`, `Schema__MGraph__Edge`

#### 2. Model Layer
- Implements business logic and data manipulation
- Depends only on Schema layer
- Returns only Model objects
- Encapsulates Schema objects
- Handles validation and type conversion
- Example: `Model__MGraph__Node`, `Model__MGraph__Edge`

#### 3. Domain Layer
- Implements high-level application logic
- Depends only on Model layer 
- Returns only Domain objects
- Handles domain-specific operations and workflows
- Example: `MGraph__Node`, `MGraph__Edge`

### Key Design Principles

1. **Unidirectional Dependencies**
   - Lower layers must not know about higher layers
   - Schema layer is self-contained
   - Model layer only knows about Schema
   - Domain layer only knows about Model

2. **Type Isolation**
   - Each layer only returns objects of its own level
   - Schema → Schema objects
   - Model → Model objects (never Schema objects)
   - Domain → Domain objects (never Model or Schema objects)
   - Higher layers encapsulate lower layer objects

3. **Clear Boundaries**
   - Explicit interfaces between layers
   - No leaking of implementation details
   - Strong encapsulation within each layer

### Component Organization

1. **Schema Components**
   ```python
   class Schema__MGraph__Node(Type_Safe):
       # Only primitive types and other schemas
       node_id: Random_Guid
       value: Any
   ```

2. **Model Components**
   ```python
   class Model__MGraph__Node:
       # Only schema dependencies
       data: Schema__MGraph__Node
       
       def value(self) -> Any:
           return self.data.value
   ```

3. **Domain Components**
   ```python
   class MGraph__Node:
       # Only model dependencies
       node: Model__MGraph__Node
       
       def value(self) -> Any:
           return self.node.value()
   ```

### Implementation Guidelines

1. **Schema Layer**
   - No business logic
   - Only type definitions and basic validation
   - No external dependencies except for type definitions
   - Must be serializable

2. **Model Layer**
   - Basic business logic
   - Data validation and manipulation
   - Depends only on Schema layer
   - Returns only Model objects
   - Encapsulates Schema objects internally
   - Handles type conversion

3. **Domain Layer**
   - Complex business logic
   - High-level operations
   - Workflow orchestration
   - External system integration

### Testing Strategy

1. **Schema Tests**
   - Focus on type validation
   - Test serialization/deserialization
   - Verify constraints

2. **Model Tests**
   - Test business logic
   - Verify data manipulation
   - Test validation rules

3. **Domain Tests**
   - Test workflows
   - Verify high-level operations
   - Test integration scenarios

### Error Handling

1. **Schema Layer**
   - Type validation errors
   - Constraint violations
   - Serialization errors

2. **Model Layer**
   - Business rule violations
   - Data validation errors
   - State transition errors

3. **Domain Layer**
   - Workflow errors
   - Integration errors
   - Business process errors

### Benefits

1. **Maintainability**
   - Clear separation of concerns
   - Isolated changes
   - Easy to understand dependencies

2. **Testability**
   - Each layer can be tested independently
   - Clear boundaries for mocking
   - Isolated test scenarios

3. **Flexibility**
   - Easy to modify implementation details
   - Simple to add new features
   - Clear upgrade paths

### Common Pitfalls to Avoid

1. **Breaking Layer Isolation**
   ```python
   # BAD: Domain layer using Schema directly
   class MGraph__Node:
       def __init__(self, schema: Schema__MGraph__Node): ...
   
   # GOOD: Domain layer using Model
   class MGraph__Node:
       def __init__(self, node: Model__MGraph__Node): ...
   ```

2. **Leaking Implementation Details**
   ```python
   # BAD: Exposing schema internals
   class Model__MGraph__Node:
       def get_raw_data(self) -> Schema__MGraph__Node: ...
   
   # GOOD: Maintaining abstraction
   class Model__MGraph__Node:
       def value(self) -> Any: ...
   ```

3. **Circular Dependencies**
   ```python
   # BAD: Cross-layer dependencies
   class Schema__MGraph__Node:
       model: Model__MGraph__Node  # WRONG!
   
   # GOOD: Maintaining hierarchy
   class Schema__MGraph__Node:
       node_id: Random_Guid
   ```

### Best Practices

1. **Clear Naming**
   - Schema classes: `Schema__*`
   - Model classes: `Model__*`
   - Domain classes: `MGraph__*`

2. **Type Safety**
   - Use type hints consistently
   - Validate at layer boundaries
   - Document type constraints

3. **Error Handling**
   - Define clear error hierarchies
   - Handle errors at appropriate layers
   - Maintain error context

4. **Documentation**
   - Document layer responsibilities
   - Specify type contracts
   - Explain validation rules

### Migration Path

When adding new features:

1. Start with Schema layer
   - Define data structures
   - Add type definitions
   - Implement validation

2. Build Model layer
   - Implement business logic
   - Add data manipulation
   - Handle validation

3. Create Domain layer
   - Add high-level operations
   - Implement workflows
   - Handle integration

### Conclusion

This architecture provides a robust foundation for building maintainable and scalable graph-based applications. The strict layering and clear responsibilities make it easy to understand, test, and extend the system while maintaining code quality and type safety.
