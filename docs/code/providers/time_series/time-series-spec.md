# MGraph TimeSeries Technical Specification

## Introduction

MGraph TimeSeries is a specialized graph representation for temporal data that treats time components as first-class graph elements. This design enables powerful temporal queries, efficient storage through component reuse, and natural support for multilingual representations and various time formats.

## Core Design Philosophy

The fundamental principle is treating temporal values as nodes connected by semantic relationships rather than as embedded properties. This approach:

1. **Makes Time Graph-Native**: 
   - Each time component (year, month, day, etc.) becomes a node
   - Relationships between components are explicit edges
   - Values are shared and reused across multiple timestamps

2. **Separates Values from Meaning**:
   - Numbers like "1" can represent different concepts (day, month, hour)
   - Edge types ("month", "day", "hour") provide semantic meaning
   - Allows efficient reuse of common values

3. **Supports Rich Metadata**:
   - Names and formatting are connected via edges
   - Natural support for internationalization
   - Extensible for additional metadata

## Architecture Overview

### File Structure
```
my_data.mgraph.json               # Main data graph
my_data.timeseries.mgraph.json    # Associated temporal graph
```

### Core Components

1. **Value Nodes**:
```
Schema__MGraph__Node__Value__Int  # Numeric values
Schema__MGraph__Node__Value__Str  # String values (names, formats)
```

2. **Time Edges**:
```
Schema__MGraph__TimeSeries__Edge__Year
Schema__MGraph__TimeSeries__Edge__Month
Schema__MGraph__TimeSeries__Edge__Day
Schema__MGraph__TimeSeries__Edge__Hour
Schema__MGraph__TimeSeries__Edge__Minute
Schema__MGraph__TimeSeries__Edge__Second
Schema__MGraph__TimeSeries__Edge__Name
Schema__MGraph__TimeSeries__Edge__Format
Schema__MGraph__TimeSeries__Edge__Language
```

### Graph Structure Example

```
TIME_SERIES_NODE(ts_id_123)  -->["year"]-->  VALUE_INT(2025)
                             -->["month"]--> VALUE_INT(2) -->["name_en"]--> VALUE_STR("February")
                                                         -->["name_pt"]--> VALUE_STR("Fevereiro")
                             -->["day"]-->   VALUE_INT(1)
                             -->["hour"]-->  VALUE_INT(13)
                             -->["minute"]--> VALUE_INT(44)
```

## Key Features

### 1. Value Reuse
- Common values (1-31 for days, 1-12 for months) are stored once
- Multiple timestamps can reference the same value nodes
- Reduces storage requirements and improves query efficiency

### 2. Multilingual Support
```
VALUE_INT(1) -->["name_en"]--> VALUE_STR("January")
           -->["name_es"]--> VALUE_STR("Enero")
           -->["name_pt"]--> VALUE_STR("Janeiro")
```

### 3. Format Flexibility
```
VALUE_INT(13) -->["format_24h"]--> VALUE_STR("13")
            -->["format_12h"]--> VALUE_STR("1")
            -->["period"]-----> VALUE_STR("PM")
```

### 4. Cross-Graph Linking
```
// In articles.mgraph.json
ARTICLE(article_123) -->["published"]--> TIME_SERIES(ts_id_123)

// In articles.timeseries.mgraph.json
TIME_SERIES(ts_id_123) // Full temporal representation
```

## Implementation Benefits

1. **Efficient Queries**:
   - Find all events at a specific hour across dates
   - Group by any time component
   - Complex temporal pattern matching

2. **Natural Visualization**:
   - Graph structure reveals temporal patterns
   - Clear representation of time hierarchies
   - Visual insights into data distribution

3. **Extensible Design**:
   - Easy to add new time components
   - Support for different calendar systems
   - Custom time representations

4. **Analytics Support**:
   - Time-based aggregations
   - Trend analysis
   - Pattern detection

## Use Cases

1. **Content Management**:
   - Article publication timestamps
   - Content revision history
   - Scheduling and planning

2. **Event Tracking**:
   - User activity timelines
   - System event logging
   - Time-based metrics

3. **Time Series Analysis**:
   - Performance metrics
   - Usage patterns
   - Trend identification

## Visual Representation

The graph structure naturally lends itself to visualization:

1. **Temporal Hierarchies**:
   - Year → Month → Day → Hour structure
   - Clear parent-child relationships
   - Visual pattern recognition

2. **Value Distribution**:
   - Popular time periods become visually apparent
   - Usage patterns emerge naturally
   - Temporal clustering becomes visible

3. **Relationship Networks**:
   - Connections between events
   - Temporal dependencies
   - Pattern visualization

## Next Steps

1. **Implementation**:
   - Core node and edge schemas
   - Edit and query interfaces
   - Visualization components

2. **Documentation**:
   - API reference
   - Usage examples
   - Best practices

3. **Testing**:
   - Unit tests
   - Performance benchmarks
   - Use case validation