# MGraph Time Series Sequential Architecture

## Problem Statement

### Current Implementation
The current MGraph Time Series implementation uses a hub-and-spoke model where:
- A central time point node connects to individual value nodes
- Each value node represents a time component (year, month, day, etc.)
- Edges are typed to indicate the component type (year_edge, month_edge, etc.)
- Values are reused through the MGraph value node system

Example hub-and-spoke structure for "2025-02-18 11:22:59":
```
                        [Year: 2025]
                        [Month: 2]
TimePoint --> [Day: 18]
                        [Hour: 11]
                        [Minute: 22]
                        [Second: 59]
```

### Limitations
1. No natural sequence between components
2. Cannot easily find all time points for a given year/month/day
3. Inefficient querying of time ranges
4. No clear representation of time hierarchy

### Requirements
1. Maintain efficient value reuse
2. Preserve existing serialization format
3. Enable efficient time-based queries
4. Support clear time component hierarchy
5. Allow sharing of common time paths

## Solution Architecture

### Core Concept
Transform the hub-and-spoke model into a sequential chain where:
- Each node represents a position in the time sequence
- Nodes are connected through typed edges
- Value reuse is maintained through the existing value node system
- Node types indicate their position in sequence

### Key Components

#### 1. Type Markers
Simple classes that serve as type indicators in value nodes:
```python
class Year(str): pass
class Year_Month(str): pass
class Year_Month_Day(str): pass
class Year_Month_Day_Hour(str): pass
class Year_Month_Day_Hour_Minute(str): pass
class Year_Month_Day_Hour_Minute_Second(str): pass
```

#### 2. Edge Types
Specialized edges to connect sequence components:
```python
class Schema__MGraph__Time_Series__Edge__Year(Schema__MGraph__Edge): pass
class Schema__MGraph__Time_Series__Edge__Month(Schema__MGraph__Edge): pass
class Schema__MGraph__Time_Series__Edge__Day(Schema__MGraph__Edge): pass
class Schema__MGraph__Time_Series__Edge__Hour(Schema__MGraph__Edge): pass
class Schema__MGraph__Time_Series__Edge__Minute(Schema__MGraph__Edge): pass
class Schema__MGraph__Time_Series__Edge__Second(Schema__MGraph__Edge): pass
```

#### 3. Value Node Integration
Utilizes existing Schema__MGraph__Node__Value__Data:
```python
class Schema__MGraph__Node__Value__Data(Type_Safe):
    value     : str   # Actual component value (e.g., "2025", "2", "18")
    value_type: Type  # Type marker (e.g., Year, Year_Month)
```

### Sequential Structure Example
For datetime "2025-02-18 11:22:59":
```
[Year("2025")] -> [Year_Month("2")] -> [Year_Month_Day("18")] -> 
[Year_Month_Day_Hour("11")] -> [Year_Month_Day_Hour_Minute("22")] ->
[Year_Month_Day_Hour_Minute_Second("59")]
```

### Value Reuse Mechanism

1. Node Creation:
```python
# Create month node
month_node = mgraph_edit.new_node(node_type=Schema__MGraph__Node__Value)
month_node.node_data.value = "2"              # Direct value
month_node.node_data.value_type = Year_Month  # Type marker
```

2. Value Reuse:
- Reuse handled by MGraph__Index__Values
- Hash calculated from value + value_type
- Same components automatically share nodes

Example of reuse:
```
2025-02-18 11:22:59
           ↳ [Year(2025)] → [Month(2)] → [Day(18)] → [Hour(11)]
           
2025-02-18 14:30:00
           ↳ [Year(2025)] → [Month(2)] → [Day(18)] → [Hour(14)]
```
Common nodes (2025, 2, 18) are reused.

### Serialization

Each node serializes to:
```json
{
    "node_id": "unique_id",
    "node_data": {
        "value": "2",
        "value_type": "Year_Month"
    }
}
```

### Benefits

1. Efficient Storage
- Reuses common time components
- Minimal node duplication
- Standard value node storage

2. Clear Time Hierarchy
- Natural sequence representation
- Easy to traverse time paths
- Clear component relationships

3. Query Efficiency
- Find all times for year/month
- Navigate time sequences
- Range queries supported

4. Maintainability
- Uses existing infrastructure
- Simple serialization
- Clear type system

## Implementation Examples

### 1. Creating Time Sequence
```python
def create_sequence(year: int, month: int, day: int):
    # Create value nodes with type markers
    year_node = values.get_or_create_with_type(
        value=str(year),
        value_type=Year
    )
    
    month_node = values.get_or_create_with_type(
        value=str(month),
        value_type=Year_Month
    )
    
    # Link in sequence
    mgraph.new_edge(
        edge_type=Schema__MGraph__Time_Series__Edge__Month,
        from_node_id=year_node.node_id,
        to_node_id=month_node.node_id
    )
```

### 2. Finding Time Points
```python
def find_time_points(year: int, month: int):
    # Find year node
    year_node = values.get_node_by_value(
        value=str(year),
        value_type=Year
    )
    
    # Follow sequence
    month_nodes = graph.get_nodes_connected_to_node(
        node_id=year_node.node_id,
        edge_type=Schema__MGraph__Time_Series__Edge__Month
    )
```

## Design Principles

1. Value Reuse
- Utilize existing value node system
- Maintain unique instances
- Share common components

2. Type Safety
- Clear type markers
- Typed edges
- Validated sequences

3. Efficient Storage
- Minimal duplication
- Standard serialization
- Compact representation

4. Query Optimization
- Direct path access
- Component reuse
- Range support

## Migration Path

1. Convert existing time points:
- Extract components from hub-and-spoke
- Create sequential structure
- Maintain original time points
- Verify component matching

2. Update creation process:
- Implement sequential creation
- Ensure value reuse
- Add validation
- Update queries

## Next Steps

1. Implementation
- Create type markers
- Add edge types
- Implement creation logic
- Add query methods

2. Testing
- Value reuse verification
- Sequence integrity
- Query performance
- Migration testing

3. Documentation
- API documentation
- Usage examples
- Query patterns
- Best practices