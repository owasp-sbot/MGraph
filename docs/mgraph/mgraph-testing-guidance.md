# MGraph Testing Best Practices and Patterns

## Context Manager Usage

### Using Type_Safe's Context Manager

All Type_Safe instances have context manager support. Always use it for cleaner, more readable code:

```python
# DON'T DO THIS - verbose and harder to read
assert type(self.model) is Model__File_System__Graph
assert self.model.some_value == expected_value

# DO THIS INSTEAD - cleaner and more maintainable
with self.model as _:
    assert type(_) is Model__File_System__Graph
    assert _.some_value == expected_value
```

## Type_Safe Object Creation

### Let Type_Safe Handle Defaults

The `Type_Safe` class automatically handles creation of typed attributes with their default values. Don't explicitly set these unless needed.

```python
# DON'T DO THIS - unnecessarily verbose
self.item = Schema__File_System__Item(
    folder_name = self.folder_name,
    node_config = Schema__Node__Config(node_id=Random_Guid()),  # Not needed
    attributes  = {}                                            # Not needed
)

# DO THIS INSTEAD - clean and concise
self.item  = Schema__File_System__Item(folder_name = self.folder_name)
self.model = Model__File_System__Item (data        = self.item       )
```

### Alignment Patterns

Always align `=` signs and parentheses in related statements:

```python
self.item  = Schema__File_System__Item(folder_name = self.folder_name)
self.model = Model__File_System__Item (data        = self.item       )
```

## Testing Extended Classes

### Testing Overridden Methods

When testing a class that extends a base class (e.g., `Model__MGraph__Graph`), explicitly test the overridden methods:

1. Test type registrations
2. Verify correct class creation
3. Check inheritance chain

Example testing `new_node`:
```python
def test_new_node(self):
    with self.model as _:
        assert type(_)                        is Model__File_System__Graph
        assert _.node_model_type              is Model__File_System__Item
        assert _.data.default_types.node_type is Schema__File_System__Item
        node = _.new_node()
        assert type(node)                     is Model__File_System__Item
```

Example testing `new_edge`:
```python
def test_new_edge(self):
    with self.model as _:
        node_1_id = _.new_node().node_id()
        node_2_id = _.new_node().node_id()
        edge      = _.new_edge(from_node_id=node_1_id, to_node_id=node_2_id)
        
        assert _.edge_model_type              is Model__MGraph__Edge
        assert _.data.default_types.edge_type is Schema__MGraph__Edge                        
        assert type(edge)                     is Model__MGraph__Edge
```

### Default Types Configuration

When extending base classes, ensure proper type registration through Default Types classes:

```python
class Schema__File_System__Default__Types(Schema__MGraph__Default__Types):
    edge_type        : Type[Schema__MGraph__Edge              ]
    edge_config_type : Type[Schema__MGraph__Edge__Config      ]
    graph_config_type: Type[Schema__File_System__Graph__Config]
    node_type        : Type[Schema__File_System__Item         ]
    node_config_type : Type[Schema__MGraph__Node__Config      ]
```

Wire up in the graph class:
```python
class Schema__File_System__Graph(Schema__MGraph__Graph):
    default_types : Schema__File_System__Default__Types
    graph_config  : Schema__File_System__Graph__Config
```

## Test Methods

### Initialization Tests

The `test_init` method should be thorough and explicit. Key patterns:

1. Use context manager
2. Capture current state before assertions
3. Test types explicitly
4. Verify timestamps are reasonable
5. Use `obj()` for complete state verification
6. Test all auto-generated fields

Example pattern:
```python
def test_init(self):                                                              # Tests basic initialization
    with self.model as _:
        timestamp_now = timestamp_utc_now()
        node_id       = _.node_id    ()
        created_at    = _.created_at ()
        modified_at   = _.modified_at()
        node_type     = full_type_name(_.data.node_type)
        
        assert type(_)                is Model__File_System__Item
        assert _.data.node_type       is Schema__File_System__Item
        assert _.folder_name()        == self.folder_name
        assert _.created_at ()        is not None
        assert _.modified_at()        is not None
        assert is_guid(node_id)       is True
        assert type(created_at)       is Timestamp_Now
        assert type(modified_at)      is Timestamp_Now
        assert isinstance(created_at, int) is True
        assert timestamp_now - 5 <= modified_at <= timestamp_now
        assert timestamp_now - 5 <= created_at  <= timestamp_now
        
        # Complete state verification using obj()
        assert _.obj() == __(data=__(folder_name  = self.folder_name       ,
                                   created_at   = created_at              ,
                                   modified_at  = modified_at             ,
                                   attributes   = __()                    ,
                                   node_config  = __(node_id    = node_id,
                                                   value_type = None    ),
                                   node_type    = node_type              ,
                                   value        = None                   ))
```

## Object State Verification

### Using the `__` Class

The `__` class (based on `SimpleNamespace`) provides clean object state verification:

```python
class __(SimpleNamespace):
    pass
```

Use `obj()` with `__` for complete state verification instead of checking individual attributes.

## Graph Initialization

### Minimal Graph Creation

Unless you need specific configuration values, prefer the most concise initialization:

```python
# DON'T DO THIS - unnecessarily verbose
self.graph__schema = Schema__File_System__Graph__Config(graph_id=Random_Guid())
self.graph = Schema__File_System__Graph(
    graph_config=self.graph__schema,
    nodes={},
    edges={}
)

# DO THIS INSTEAD - concise
self.graph = Schema__File_System__Graph()

# OR EVEN MORE CONCISE when only model is needed
self.model = Model__File_System__Graph()
```

### When to Keep Configuration References

Only keep references to configuration objects when you need to:
1. Access their values later in tests
2. Modify their values as part of test scenarios
3. Verify specific configuration states

## General Best Practices

1. **Use Context Managers**: Always use Type_Safe's context manager with `_` convention
2. **Minimal Setup**: Only initialize what's needed for the specific test
3. **Explicit Testing**: Be thorough in type and value verification
4. **Alignment**: Maintain consistent alignment patterns
5. **Comments**: Include descriptive comments for test methods
6. **State Verification**: Use `obj()` for complete state checks
7. **Time Testing**: Use reasonable timestamp ranges for verification
8. **Type Checking**: Test both direct types and inheritance
9. **Extended Classes**: Explicitly test overridden methods and type registration