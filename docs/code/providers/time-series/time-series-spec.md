# MGraph TimeSeries Technical Specification

## Introduction

MGraph TimeSeries is a specialized graph representation for temporal data that treats time components as first-class graph elements. By representing each temporal component as a node and using edges for semantic relationships, this design enables powerful temporal queries, efficient storage through value reuse, and natural support for multilingual representations.

## Core Design Philosophy

### 1. Graph-Native Time Representation

The fundamental principle is treating temporal values as nodes connected by semantic relationships rather than as embedded properties:

```
TIME_POINT_1 --["year"]-->  VALUE(2025)
             --["month"]--> VALUE(2)   --["name_en"]--> VALUE("February")
                                      --["name_pt"]--> VALUE("Fevereiro")
             --["day"]-->   VALUE(1)   --["name_en"]--> VALUE("First")
                                      --["ordinal"]--> VALUE("1st")
```

Benefits:
- Pure graph representation - no embedded properties
- Each component is independently queryable
- Natural support for metadata and relationships
- Efficient value reuse across timestamps

### 2. File Structure and Graph Separation

```
articles.mgraph.json               # Main data graph
articles.timeseries.mgraph.json    # Temporal graph
```

This separation provides:
- Clear separation of concerns
- Independent optimization of each graph
- Flexible cross-graph relationships
- Improved query performance
- Easier maintenance and updates

### 3. Cross-Graph Linking

Example of how articles and time points connect:

```
// In articles.mgraph.json
ARTICLE(article_123) --["published"]--> TIME_SERIES(ts_id_123)
                     --["updated"]---> TIME_SERIES(ts_id_124)

// In articles.timeseries.mgraph.json
TIME_SERIES(ts_id_123)  -->["year"]-->  VALUE(2025)
                        -->["month"]--> VALUE(2)
                        -->["day"]-->   VALUE(1)
```

## Technical Implementation

### 1. Core Components

#### Value Nodes
```python
class Schema__MGraph__Node__Value(Schema__MGraph__Node):
    """Base class for all value nodes"""
    node_data: Schema__MGraph__Node__Value__Data

class Schema__MGraph__Node__Value__Int(Schema__MGraph__Node__Value):
    value: int   # For years, months, days, hours, etc.
    
class Schema__MGraph__Node__Value__Str(Schema__MGraph__Node__Value):
    value: str   # For names, formats, etc.
```

#### Edge Types
```python
# Temporal Components
class Schema__MGraph__TimeSeries__Edge__Year(Schema__MGraph__Edge): pass
class Schema__MGraph__TimeSeries__Edge__Month(Schema__MGraph__Edge): pass
class Schema__MGraph__TimeSeries__Edge__Day(Schema__MGraph__Edge): pass
class Schema__MGraph__TimeSeries__Edge__Hour(Schema__MGraph__Edge): pass

# Metadata
class Schema__MGraph__TimeSeries__Edge__Name(Schema__MGraph__Edge): pass
class Schema__MGraph__TimeSeries__Edge__Format(Schema__MGraph__Edge): pass
class Schema__MGraph__TimeSeries__Edge__Language(Schema__MGraph__Edge): pass
```

### 2. Rich Examples

#### Multilingual Month Representation
```
VALUE_INT(1) --["name_en"]--> VALUE_STR("January")
           --["name_es"]--> VALUE_STR("Enero")
           --["name_pt"]--> VALUE_STR("Janeiro")
           --["short_name_en"]--> VALUE_STR("Jan")
```

#### Time Format Variations
```
VALUE_INT(13) --["format_24h"]--> VALUE_STR("13")
            --["format_12h"]--> VALUE_STR("1")
            --["period"]-----> VALUE_STR("PM")
            --["spoken"]-----> VALUE_STR("one o'clock")
```

#### Complete Time Point Example
```
TIME_POINT --["year"]---> VALUE(2025)
          --["month"]--> VALUE(2) --["name"]--> VALUE("February")
          --["day"]---> VALUE(1) --["name"]--> VALUE("Saturday")
          --["hour"]--> VALUE(13)
          --["minute"]--> VALUE(44)
          --["timezone"]--> VALUE(330) --["format"]--> VALUE("+0530")
```

## Query Capabilities

### 1. Basic Temporal Queries
```python
def find_weekends(self) -> List[Obj_Id]:
    """Find all weekend time points"""
    weekend_days = self.index().get_nodes_by_field('name', 
                                                  ['Saturday', 'Sunday'])
    return self._get_connected_time_points(weekend_days, 
                                         Schema__MGraph__TimeSeries__Edge__Day)

def find_working_hours(self) -> List[Obj_Id]:
    """Find time points during working hours (9-17)"""
    return self.find_hour_range(9, 17)
```

### 2. Complex Pattern Matching
```python
def find_pattern(self, pattern: Dict[str, Any]) -> List[Obj_Id]:
    """Find time points matching a specific pattern
    
    Example:
    pattern = {
        'month': 2,             # February
        'day_type': 'weekend',  # Weekend days
        'hour_range': (9, 17)   # Working hours
    }
    """
```

### 3. Cross-Graph Queries
```python
def find_articles_published_on_weekends(self) -> List[Obj_Id]:
    """Find articles published on weekends"""
    weekend_times = self.find_weekends()
    return self.find_linked_articles(weekend_times, "published")
```

## Value Reuse and Optimization

### 1. Value Node Registry
```python
class ValueNodeRegistry:
    """Manages unique value nodes"""
    
    def get_or_create_value(self, value: Any) -> Obj_Id:
        """Returns existing value node or creates new one"""
        
    def get_or_create_named_value(self, value: Any, 
                                 names: Dict[str, str]) -> Obj_Id:
        """Creates value node with multilingual names"""
```

### 2. Performance Optimizations
- Shared value nodes for common numbers (1-31 for days)
- Cached metadata for frequent values
- Optimized index structures for temporal queries
- Efficient cross-graph reference resolution

## Visual Representation

### 1. Natural Visualization Benefits

The graph structure naturally reveals:
- Temporal hierarchies (Year → Month → Day → Hour)
- Value distribution patterns
- Usage frequency of time components
- Temporal clustering
- Cross-graph relationships
- Event patterns and sequences

### 2. Visual Patterns
```
TIME_POINT_1 --["hour"]--> VALUE(9)
TIME_POINT_2 --["hour"]--> VALUE(9)  // Pattern: Same hour
TIME_POINT_3 --["hour"]--> VALUE(9)  // Clear visual cluster
```

## Common Use Cases

### 1. Content Management
- Article publication timestamps
- Content revision history
- Scheduled publications
- Content lifecycle tracking
- Temporal content relationships

### 2. Event Tracking
- User activity timelines
- System event logging
- Audit trails
- Session analysis
- Temporal pattern detection

### 3. Time Series Analysis
- Performance metrics
- Usage patterns
- Trend identification
- Seasonal patterns
- Anomaly detection

### 4. Cross-Domain Analysis
- Content popularity by time
- User behavior patterns
- System load patterns
- Correlation analysis

## Implementation Roadmap

### Phase 1: Core Framework
- Basic node and edge types
- Value registry implementation
- Simple temporal queries
- Cross-graph linking

### Phase 2: Advanced Features
- Multilingual support
- Complex query patterns
- Pattern matching
- Time range operations

### Phase 3: Optimization
- Value node reuse
- Index structures
- Query optimization
- Performance tuning

### Phase 4: Visualization
- Temporal layout algorithms
- Pattern visualization
- Interactive exploration
- Visual analytics

## Future Extensions

### 1. Advanced Analytics
- Time series forecasting
- Pattern recognition
- Anomaly detection
- Trend analysis

### 2. Integration Features
- External time series data
- Real-time updates
- Streaming support
- Data synchronization

### 3. Specialized Use Cases
- Calendar systems
- Holiday patterns
- Business hours
- Time zone handling
- Custom temporal patterns

## Best Practices

### 1. Data Modeling
- Use appropriate value types
- Maintain consistent edge patterns
- Leverage value reuse
- Design for querying

### 2. Query Optimization
- Use appropriate indexes
- Cache common queries
- Optimize traversal patterns
- Monitor performance

### 3. Cross-Graph Design
- Clear separation of concerns
- Efficient linking patterns
- Consistent ID management
- Transaction handling

## Testing Strategy

### 1. Unit Tests
- Component creation
- Query operations
- Value reuse
- Edge cases

### 2. Integration Tests
- Cross-graph operations
- Complex queries
- Performance benchmarks
- Data consistency

### 3. Visual Testing
- Layout verification
- Pattern recognition
- Visual insights
- User interaction