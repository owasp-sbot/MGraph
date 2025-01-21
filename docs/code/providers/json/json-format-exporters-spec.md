# MGraph_Json - Format Exporters - Technical Specification

## Introduction

The MGraph system's power lies in its ability to represent complex data structures as graphs while maintaining flexibility in how this data can be viewed and manipulated. A critical aspect of this flexibility is the ability to export graph representations into various standard formats, each serving different use cases and integration needs.

### Purpose

This technical specification defines the implementation approach for MGraph format exporters, which transform internal graph representations into standard graph formats. These exporters serve several key purposes:

1. **Visualization**: Formats like DOT and GEXF enable graph visualization through tools like Graphviz and Gephi
2. **Data Exchange**: Formats like GraphML and CSV facilitate data exchange with other systems
3. **Semantic Web Integration**: RDF/Turtle and N-Triples support semantic web applications
4. **Database Integration**: Neo4j Cypher enables direct database imports
5. **Analysis**: Various formats support different analysis tools and approaches

### Design Philosophy

The format exporters follow these key principles:

1. **Format-First**: Each exporter prioritizes the idioms and best practices of its target format
2. **Simplicity**: Complex internal structures are simplified for external consumption
3. **Readability**: Generated output emphasizes human readability where possible
4. **Flexibility**: Support format-specific features while maintaining core graph semantics

### Scope

This specification covers:
- Detailed format examples with complex test cases
- Implementation guidelines and best practices
- Common patterns and shared functionality
- Format-specific considerations and requirements
- Error handling and validation approaches

### Target Formats

The specification includes these standard formats:
- DOT Graph Language
- RDF/Turtle
- N-Triples
- GraphML
- GEXF (Graph Exchange XML Format)
- TGF (Trivial Graph Format)
- Neo4j Cypher
- CSV (Multiple Files)

## Core Design Principles

1. **Format-First Design**
   - Each exporter optimizes for the target format's idioms and best practices
   - Willing to sacrifice data fidelity for format clarity
   - Follow each format's conventions and common patterns
   - Optimize for human readability in text formats

2. **Simplified Identifiers**
   - Use truncated GUIDs (first segment only)
   - Example: `e0fe637f-3341-4e2a-a06d-46b71e94d32f` → `e0fe637f`
   - Omit IDs entirely when the format doesn't require them
   - Use format-specific ID conventions when appropriate

3. **Minimal Data Transfer**
   - Export only essential structural information
   - Focus on topology over metadata
   - Preserve only format-relevant attributes
   - Avoid cluttering exports with internal details

## File Organization

Each format should have its own dedicated exporter class:

```
mgraph_ai/
  providers/
    json/
      exporters/
        MGraph__Json__Export__Dot.py
        MGraph__Json__Export__Turtle.py
        MGraph__Json__Export__NTriples.py
        MGraph__Json__Export__GraphML.py
        MGraph__Json__Export__GEXF.py
        MGraph__Json__Export__TGF.py
        MGraph__Json__Export__Cypher.py
        MGraph__Json__Export__CSV.py
```

## Format-Specific Guidelines

## Rich Example Case

To demonstrate how each format handles complex JSON structures, we'll use this comprehensive test data:

```json
{
    "string": "value",
    "number": 42,
    "boolean": true,
    "null": null,
    "array": [1, 2, 3],
    "object": {
        "key": "value"
    }
}
```

This test case includes:
- Primitive values (string, number, boolean, null)
- Array with multiple elements
- Nested object structure
- Multiple property types

The MGraph JSON representation of this data creates:
- A root dictionary node
- Property nodes for each top-level key
- Value nodes for primitives
- List node for array
- Dictionary node for nested object
- Additional property and value nodes for nested structures

### 1. DOT Graph Format

The DOT format emphasizes graph visualization and should prioritize readability.

**Key Principles:**
- Use meaningful node labels when available
- Apply consistent formatting for readability
- Include minimal but useful attributes
- Leverage DOT's visual capabilities

**DOT Export Example:**
```dot
digraph {
    // Root dictionary node
    root [shape=record, label="root"]
    
    // Property nodes
    p_string  [label="string"]
    p_number  [label="number"]
    p_boolean [label="boolean"]
    p_null    [label="null"]
    p_array   [label="array"]
    p_object  [label="object"]
    
    // Value nodes
    v_string  [label="value"]
    v_number  [label="42"]
    v_boolean [label="true"]
    v_null    [label="null"]
    
    // Array values
    array_node [shape=record, label="array"]
    v_array1   [label="1"]
    v_array2   [label="2"]
    v_array3   [label="3"]
    
    // Nested object
    object_node    [shape=record, label="object"]
    p_object_key   [label="key"]
    v_object_value [label="value"]
    
    // Connect root to properties
    root -> p_string
    root -> p_number
    root -> p_boolean
    root -> p_null
    root -> p_array
    root -> p_object
    
    // Connect properties to values
    p_string  -> v_string
    p_number  -> v_number
    p_boolean -> v_boolean
    p_null    -> v_null
    p_array   -> array_node
    p_object  -> object_node
    
    // Array connections
    array_node -> v_array1
    array_node -> v_array2
    array_node -> v_array3
    
    // Nested object connections
    object_node  -> p_object_key
    p_object_key -> v_object_value
    
    // Visual settings
    node [style=filled, fillcolor=lightgrey]
}

**DOT Output:**
```dot
digraph {
  // Node definitions with shortened IDs
  e0fe637f [label="Start"]
  f1fe637f [label="End"]
  
  // Edge definitions
  e0fe637f -> f1fe637f
}
```

### 2. RDF/Turtle Format

Turtle format should focus on semantic relationships and clear predicate definitions.

**Example Output:**
```turtle
@prefix mg: <http://mgraph.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Root node
mg:root a mg:Object .

# Property nodes
mg:p_string  a mg:Property ; mg:name "string" .
mg:p_number  a mg:Property ; mg:name "number" .
mg:p_boolean a mg:Property ; mg:name "boolean" .
mg:p_null    a mg:Property ; mg:name "null" .
mg:p_array   a mg:Property ; mg:name "array" .
mg:p_object  a mg:Property ; mg:name "object" .

# Value nodes with typed literals
mg:v_string  mg:hasValue "value" .
mg:v_number  mg:hasValue "42"^^xsd:integer .
mg:v_boolean mg:hasValue "true"^^xsd:boolean .
mg:v_null    mg:hasValue mg:null .

# Array structure
mg:array_node a mg:Array ;
    mg:item [ mg:index "0" ; mg:value "1"^^xsd:integer ] ;
    mg:item [ mg:index "1" ; mg:value "2"^^xsd:integer ] ;
    mg:item [ mg:index "2" ; mg:value "3"^^xsd:integer ] .

# Nested object
mg:object_node a mg:Object ;
    mg:property [ 
        mg:name "key" ;
        mg:value "value"
    ] .

# Root connections
mg:root mg:property mg:p_string .
mg:root mg:property mg:p_number .
mg:root mg:property mg:p_boolean .
mg:root mg:property mg:p_null .
mg:root mg:property mg:p_array .
mg:root mg:property mg:p_object .

# Property-value connections
mg:p_string  mg:hasValue mg:v_string .
mg:p_number  mg:hasValue mg:v_number .
mg:p_boolean mg:hasValue mg:v_boolean .
mg:p_null    mg:hasValue mg:v_null .
mg:p_array   mg:hasValue mg:array_node .
mg:p_object  mg:hasValue mg:object_node .
```

### 3. N-Triples Format

N-Triples should maintain absolute simplicity and literal representation.

**Example Output:**
```n-triples
<urn:root> <urn:type> <urn:Object> .

# Properties
<urn:p_string> <urn:name> "string" .
<urn:p_number> <urn:name> "number" .
<urn:p_boolean> <urn:name> "boolean" .
<urn:p_null> <urn:name> "null" .
<urn:p_array> <urn:name> "array" .
<urn:p_object> <urn:name> "object" .

# Values with types
<urn:v_string> <urn:value> "value" .
<urn:v_number> <urn:value> "42"^^<http://www.w3.org/2001/XMLSchema#integer> .
<urn:v_boolean> <urn:value> "true"^^<http://www.w3.org/2001/XMLSchema#boolean> .
<urn:v_null> <urn:value> <urn:null> .

# Array elements
<urn:array> <urn:type> <urn:Array> .
<urn:array> <urn:item0> "1"^^<http://www.w3.org/2001/XMLSchema#integer> .
<urn:array> <urn:item1> "2"^^<http://www.w3.org/2001/XMLSchema#integer> .
<urn:array> <urn:item2> "3"^^<http://www.w3.org/2001/XMLSchema#integer> .

# Nested object
<urn:object> <urn:type> <urn:Object> .
<urn:object_key> <urn:name> "key" .
<urn:object_key> <urn:value> "value" .
<urn:object> <urn:property> <urn:object_key> .

# Root connections
<urn:root> <urn:property> <urn:p_string> .
<urn:root> <urn:property> <urn:p_number> .
<urn:root> <urn:property> <urn:p_boolean> .
<urn:root> <urn:property> <urn:p_null> .
<urn:root> <urn:property> <urn:p_array> .
<urn:root> <urn:property> <urn:p_object> .

# Property-value connections
<urn:p_string> <urn:value> <urn:v_string> .
<urn:p_number> <urn:value> <urn:v_number> .
<urn:p_boolean> <urn:value> <urn:v_boolean> .
<urn:p_null> <urn:value> <urn:v_null> .
<urn:p_array> <urn:value> <urn:array> .
<urn:p_object> <urn:value> <urn:object> .
```

### 4. GraphML Format

GraphML output should leverage the format's XML structure while maintaining simplicity.

**Example Output:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns">
    <key id="d0" for="node" attr.name="type" attr.type="string"/>
    <key id="d1" for="node" attr.name="value" attr.type="string"/>
    <key id="d2" for="edge" attr.name="relationship" attr.type="string"/>
    
    <graph id="G" edgedefault="directed">
        <!-- Root node -->
        <node id="root">
            <data key="d0">object</data>
        </node>
        
        <!-- Property nodes -->
        <node id="p_string">
            <data key="d0">property</data>
            <data key="d1">string</data>
        </node>
        <node id="p_number">
            <data key="d0">property</data>
            <data key="d1">number</data>
        </node>
        <node id="p_boolean">
            <data key="d0">property</data>
            <data key="d1">boolean</data>
        </node>
        <node id="p_null">
            <data key="d0">property</data>
            <data key="d1">null</data>
        </node>
        <node id="p_array">
            <data key="d0">property</data>
            <data key="d1">array</data>
        </node>
        <node id="p_object">
            <data key="d0">property</data>
            <data key="d1">object</data>
        </node>
        
        <!-- Value nodes -->
        <node id="v_string">
            <data key="d0">value</data>
            <data key="d1">value</data>
        </node>
        <node id="v_number">
            <data key="d0">value</data>
            <data key="d1">42</data>
        </node>
        <node id="v_boolean">
            <data key="d0">value</data>
            <data key="d1">true</data>
        </node>
        <node id="v_null">
            <data key="d0">value</data>
            <data key="d1">null</data>
        </node>
        
        <!-- Array container and values -->
        <node id="array">
            <data key="d0">array</data>
        </node>
        <node id="v_array1">
            <data key="d0">value</data>
            <data key="d1">1</data>
        </node>
        <node id="v_array2">
            <data key="d0">value</data>
            <data key="d1">2</data>
        </node>
        <node id="v_array3">
            <data key="d0">value</data>
            <data key="d1">3</data>
        </node>
        
        <!-- Nested object -->
        <node id="object">
            <data key="d0">object</data>
        </node>
        <node id="p_object_key">
            <data key="d0">property</data>
            <data key="d1">key</data>
        </node>
        <node id="v_object_value">
            <data key="d0">value</data>
            <data key="d1">value</data>
        </node>
        
        <!-- Root connections -->
        <edge id="e1" source="root" target="p_string">
            <data key="d2">has_property</data>
        </edge>
        <edge id="e2" source="root" target="p_number">
            <data key="d2">has_property</data>
        </edge>
        <edge id="e3" source="root" target="p_boolean">
            <data key="d2">has_property</data>
        </edge>
        <edge id="e4" source="root" target="p_null">
            <data key="d2">has_property</data>
        </edge>
        <edge id="e5" source="root" target="p_array">
            <data key="d2">has_property</data>
        </edge>
        <edge id="e6" source="root" target="p_object">
            <data key="d2">has_property</data>
        </edge>
        
        <!-- Property-value connections -->
        <edge id="e7" source="p_string" target="v_string">
            <data key="d2">has_value</data>
        </edge>
        <edge id="e8" source="p_number" target="v_number">
            <data key="d2">has_value</data>
        </edge>
        <edge id="e9" source="p_boolean" target="v_boolean">
            <data key="d2">has_value</data>
        </edge>
        <edge id="e10" source="p_null" target="v_null">
            <data key="d2">has_value</data>
        </edge>
        <edge id="e11" source="p_array" target="array">
            <data key="d2">has_value</data>
        </edge>
        <edge id="e12" source="p_object" target="object">
            <data key="d2">has_value</data>
        </edge>
        
        <!-- Array connections -->
        <edge id="e13" source="array" target="v_array1">
            <data key="d2">item_0</data>
        </edge>
        <edge id="e14" source="array" target="v_array2">
            <data key="d2">item_1</data>
        </edge>
        <edge id="e15" source="array" target="v_array3">
            <data key="d2">item_2</data>
        </edge>
        
        <!-- Nested object connections -->
        <edge id="e16" source="object" target="p_object_key">
            <data key="d2">has_property</data>
        </edge>
        <edge id="e17" source="p_object_key" target="v_object_value">
            <data key="d2">has_value</data>
        </edge>
    </graph>
</graphml>
```

### 5. GEXF Format

GEXF format provides rich support for attributes and dynamic graphs. We'll use its attribute system to represent JSON types and values.

**Example Output:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">
    <graph defaultedgetype="directed">
        <!-- Attribute declarations -->
        <attributes class="node" mode="static">
            <attribute id="0" title="type" type="string"/>
            <attribute id="1" title="value" type="string"/>
            <attribute id="2" title="property_name" type="string"/>
        </attributes>
        
        <nodes>
            <!-- Root node -->
            <node id="root">
                <attvalues>
                    <attvalue for="0" value="object"/>
                </attvalues>
            </node>
            
            <!-- Property nodes -->
            <node id="p_string">
                <attvalues>
                    <attvalue for="0" value="property"/>
                    <attvalue for="2" value="string"/>
                </attvalues>
            </node>
            <node id="p_number">
                <attvalues>
                    <attvalue for="0" value="property"/>
                    <attvalue for="2" value="number"/>
                </attvalues>
            </node>
            <node id="p_boolean">
                <attvalues>
                    <attvalue for="0" value="property"/>
                    <attvalue for="2" value="boolean"/>
                </attvalues>
            </node>
            <node id="p_null">
                <attvalues>
                    <attvalue for="0" value="property"/>
                    <attvalue for="2" value="null"/>
                </attvalues>
            </node>
            <node id="p_array">
                <attvalues>
                    <attvalue for="0" value="property"/>
                    <attvalue for="2" value="array"/>
                </attvalues>
            </node>
            <node id="p_object">
                <attvalues>
                    <attvalue for="0" value="property"/>
                    <attvalue for="2" value="object"/>
                </attvalues>
            </node>
            
            <!-- Value nodes -->
            <node id="v_string">
                <attvalues>
                    <attvalue for="0" value="value"/>
                    <attvalue for="1" value="value"/>
                </attvalues>
            </node>
            <node id="v_number">
                <attvalues>
                    <attvalue for="0" value="value"/>
                    <attvalue for="1" value="42"/>
                </attvalues>
            </node>
            <node id="v_boolean">
                <attvalues>
                    <attvalue for="0" value="value"/>
                    <attvalue for="1" value="true"/>
                </attvalues>
            </node>
            <node id="v_null">
                <attvalues>
                    <attvalue for="0" value="value"/>
                    <attvalue for="1" value="null"/>
                </attvalues>
            </node>
            
            <!-- Array container and values -->
            <node id="array">
                <attvalues>
                    <attvalue for="0" value="array"/>
                </attvalues>
            </node>
            <node id="v_array1">
                <attvalues>
                    <attvalue for="0" value="value"/>
                    <attvalue for="1" value="1"/>
                </attvalues>
            </node>
            <node id="v_array2">
                <attvalues>
                    <attvalue for="0" value="value"/>
                    <attvalue for="1" value="2"/>
                </attvalues>
            </node>
            <node id="v_array3">
                <attvalues>
                    <attvalue for="0" value="value"/>
                    <attvalue for="1" value="3"/>
                </attvalues>
            </node>
            
            <!-- Nested object -->
            <node id="object">
                <attvalues>
                    <attvalue for="0" value="object"/>
                </attvalues>
            </node>
            <node id="p_object_key">
                <attvalues>
                    <attvalue for="0" value="property"/>
                    <attvalue for="2" value="key"/>
                </attvalues>
            </node>
            <node id="v_object_value">
                <attvalues>
                    <attvalue for="0" value="value"/>
                    <attvalue for="1" value="value"/>
                </attvalues>
            </node>
        </nodes>
        
        <edges>
            <!-- Root connections -->
            <edge id="e1" source="root" target="p_string" type="has_property"/>
            <edge id="e2" source="root" target="p_number" type="has_property"/>
            <edge id="e3" source="root" target="p_boolean" type="has_property"/>
            <edge id="e4" source="root" target="p_null" type="has_property"/>
            <edge id="e5" source="root" target="p_array" type="has_property"/>
            <edge id="e6" source="root" target="p_object" type="has_property"/>
            
            <!-- Property-value connections -->
            <edge id="e7" source="p_string" target="v_string" type="has_value"/>
            <edge id="e8" source="p_number" target="v_number" type="has_value"/>
            <edge id="e9" source="p_boolean" target="v_boolean" type="has_value"/>
            <edge id="e10" source="p_null" target="v_null" type="has_value"/>
            <edge id="e11" source="p_array" target="array" type="has_value"/>
            <edge id="e12" source="p_object" target="object" type="has_value"/>
            
            <!-- Array connections -->
            <edge id="e13" source="array" target="v_array1" type="item"/>
            <edge id="e14" source="array" target="v_array2" type="item"/>
            <edge id="e15" source="array" target="v_array3" type="item"/>
            
            <!-- Nested object connections -->
            <edge id="e16" source="object" target="p_object_key" type="has_property"/>
            <edge id="e17" source="p_object_key" target="v_object_value" type="has_value"/>
        </edges>
    </graph>
</gexf>
```

### 6. TGF (Trivial Graph Format)

TGF format is extremely simple, focusing on node IDs and connections. We'll add type information in node labels.

**Example Output:**
```
# Nodes
root Object:root
p_string Property:string
p_number Property:number
p_boolean Property:boolean
p_null Property:null
p_array Property:array
p_object Property:object
v_string Value:"value"
v_number Value:42
v_boolean Value:true
v_null Value:null
array Array
v_array1 Value:1
v_array2 Value:2
v_array3 Value:3
object Object
p_object_key Property:key
v_object_value Value:"value"
#
root p_string
root p_number
root p_boolean
root p_null
root p_array
root p_object
p_string v_string
p_number v_number
p_boolean v_boolean
p_null v_null
p_array array
p_object object
array v_array1
array v_array2
array v_array3
object p_object_key
p_object_key v_object_value
```

### 7. Neo4j Cypher

Cypher query language allows for rich property representation and labeled relationships.

**Example Output:**
```cypher
CREATE 
    // Root object
    (root:Object)
    
    // Property nodes
    ,(p_string:Property {name: 'string'})
    ,(p_number:Property {name: 'number'})
    ,(p_boolean:Property {name: 'boolean'})
    ,(p_null:Property {name: 'null'})
    ,(p_array:Property {name: 'array'})
    ,(p_object:Property {name: 'object'})
    
    // Value nodes
    ,(v_string:Value {value: 'value'})
    ,(v_number:Value {value: 42})
    ,(v_boolean:Value {value: true})
    ,(v_null:Value {value: null})
    
    // Array structure
    ,(array:Array)
    ,(v_array1:Value {value: 1})
    ,(v_array2:Value {value: 2})
    ,(v_array3:Value {value: 3})
    
    // Nested object
    ,(object:Object)
    ,(p_object_key:Property {name: 'key'})
    ,(v_object_value:Value {value: 'value'})

    // Root connections
    ,(root)-[:HAS_PROPERTY]->(p_string)
    ,(root)-[:HAS_PROPERTY]->(p_number)
    ,(root)-[:HAS_PROPERTY]->(p_boolean)
    ,(root)-[:HAS_PROPERTY]->(p_null)
    ,(root)-[:HAS_PROPERTY]->(p_array)
    ,(root)-[:HAS_PROPERTY]->(p_object)
    
    // Property-value connections
    ,(p_string)-[:HAS_VALUE]->(v_string)
    ,(p_number)-[:HAS_VALUE]->(v_number)
    ,(p_boolean)-[:HAS_VALUE]->(v_boolean)
    ,(p_null)-[:HAS_VALUE]->(v_null)
    ,(p_array)-[:HAS_VALUE]->(array)
    ,(p_object)-[:HAS_VALUE]->(object)
    
    // Array connections
    ,(array)-[:ITEM {index: 0}]->(v_array1)
    ,(array)-[:ITEM {index: 1}]->(v_array2)
    ,(array)-[:ITEM {index: 2}]->(v_array3)
    
    // Nested object connections
    ,(object)-[:HAS_PROPERTY]->(p_object_key)
    ,(p_object_key)-[:HAS_VALUE]->(v_object_value)
```

### 8. CSV Format

CSV exports split data into multiple files for nodes and edges, with clear type information.

**Example Output:**

nodes.csv:
```csv
node_id,type,property_name,value
root,object,,
p_string,property,string,
p_number,property,number,
p_boolean,property,boolean,
p_null,property,null,
p_array,property,array,
p_object,property,object,
v_string,value,,value
v_number,value,,42
v_boolean,value,,true
v_null,value,,null
array,array,,
v_array1,value,,1
v_array2,value,,2
v_array3,value,,3
object,object,,
p_object_key,property,key,
v_object_value,value,,value
```

edges.csv:
```csv
edge_id,from_node_id,to_node_id,relationship_type
e1,root,p_string,has_property
e2,root,p_number,has_property
e3,root,p_boolean,has_property
e4,root,p_null,has_property
e5,root,p_array,has_property
e6,root,p_object,has_property
e7,p_string,v_string,has_value
e8,p_number,v_number,has_value
e9,p_boolean,v_boolean,has_value
e10,p_null,v_null,has_value
e11,p_array,array,has_value
e12,p_object,object,has_value
e13,array,v_array1,array_item
e14,array,v_array2,array_item
e15,array,v_array3,array_item
e16,object,p_object_key,has_property
e17,p_object_key,v_object_value,has_value
```

## Implementation Notes

Having shown detailed examples for each format, here are some key implementation considerations:

### 1. Node Type Management

The exporter should maintain a consistent type system across formats:

```python
class NodeType:
    OBJECT   = "object"    # JSON objects
    PROPERTY = "property"  # Object properties
    VALUE    = "value"     # Primitive values
    ARRAY    = "array"     # Array containers

class ValueType:
    STRING  = "string"
    NUMBER  = "number"
    BOOLEAN = "boolean"
    NULL    = "null"
```

### 2. Relationship Types

Standard relationship types to use across formats:

```python
class RelationType:
    HAS_PROPERTY = "has_property"  # Object to property
    HAS_VALUE    = "has_value"     # Property to value
    ARRAY_ITEM   = "array_item"    # Array to item
```

### 3. ID Generation

Short, format-friendly IDs for each element:

```python
def generate_node_id(prefix: str, counter: int) -> str:
    """Generate format-friendly node IDs"""
    return f"{prefix}_{counter}"
```

### 4. Value Formatting

Consistent value formatting across formats:

```python
def format_value(value: Any) -> str:
    """Format values consistently across exports"""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float)):
        return str(value)
    return f'"{value}"'  # strings
```

### 5. Common Export Flow

Each format exporter should follow this basic flow:

1. Initialize format-specific context
2. Process root node
3. Process properties
4. Process values
5. Process arrays
6. Process nested objects
7. Generate relationships
8. Format output

Example base class:

```python
class MGraph__Json__Export__Base:
    def __init__(self, graph: Domain__MGraph__Json__Graph):
        self.graph = graph
        self.context = self._init_context()
    
    def _init_context(self) -> Dict:
        """Initialize format-specific export context"""
        return {
            'nodes': {},
            'edges': {},
            'counters': {
                'node': 0,
                'edge': 0
            }
        }
    
    def _process_node(self, node: Domain__MGraph__Json__Node) -> str:
        """Process a node and return its ID"""
        raise NotImplementedError()
    
    def _process_edge(self, from_id: str, to_id: str, type: str) -> None:
        """Process an edge between nodes"""
        raise NotImplementedError()
    
    def _format_output(self) -> str:
        """Format the final output"""
        raise NotImplementedError()
```

### 6. Format-Specific Considerations

For each format, consider:

1. **DOT Format**
   - Use subgraphs for arrays/objects
   - Apply visual styling for node types
   - Keep labels minimal

2. **RDF/Turtle**
   - Use clear predicate naming
   - Maintain proper namespacing
   - Handle datatype annotations

3. **N-Triples**
   - Maintain simple subject-predicate-object format
   - Use consistent URI patterns
   - Handle literal typing

4. **GraphML**
   - Define attribute keys
   - Use data elements for properties
   - Maintain valid XML structure

5. **GEXF**
   - Use attribute declarations
   - Apply visualization attributes
   - Handle dynamic elements

6. **TGF**
   - Keep node labels informative but brief
   - Use simple edge representation
   - Maintain readable formatting

7. **Cypher**
   - Use label-based node types
   - Apply relationship types
   - Handle property formatting

8. **CSV**
   - Split data logically
   - Use clear column headers
   - Handle value escaping

### 5. GEXF Format

GEXF should utilize its strengths in representing dynamic and hierarchical graphs.

**Example Output:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">
  <graph defaultedgetype="directed">
    <nodes>
      <node id="e0fe637f"/>
      <node id="f1fe637f"/>
    </nodes>
    <edges>
      <edge id="a2fe637f" source="e0fe637f" target="f1fe637f"/>
    </edges>
  </graph>
</gexf>
```

### 6. TGF (Trivial Graph Format)

TGF should maintain its characteristic simplicity and straightforward structure.

**Example Output:**
```
# Nodes
e0fe637f
f1fe637f
#
e0fe637f f1fe637f a2fe637f
```

### 7. Neo4j Cypher

Cypher output should follow Neo4j's idioms and query patterns.

**Example Output:**
```cypher
CREATE 
  (n1:Node {id: 'e0fe637f'}),
  (n2:Node {id: 'f1fe637f'}),
  (n1)-[r1:CONNECTS {id: 'a2fe637f'}]->(n2)
```

### 8. CSV Format

CSV output should split nodes and edges into separate files with clear headers.

**Example Output:**

nodes.csv:
```csv
node_id
e0fe637f
f1fe637f
```

edges.csv:
```csv
edge_id,from_node_id,to_node_id
a2fe637f,e0fe637f,f1fe637f
```

## Implementation Guidelines

1. **Class Structure**
```python
class MGraph__Json__Export__Format:
    def __init__(self, graph: Domain__MGraph__Json__Graph):
        self.graph = graph
    
    def to_string(self, **options) -> str:
        """Convert graph to format-specific string"""
        pass
        
    def to_file(self, file_path: str, **options) -> bool:
        """Export graph to file"""
        pass
```

2. **ID Handling**
```python
def _shorten_id(self, guid: str) -> str:
    """Extract first segment of GUID"""
    return guid.split('-')[0]
```

3. **Error Handling**
```python
class MGraph__Export__FormatError(Exception):
    """Base class for format-specific export errors"""
    pass
```

## Testing Strategy

1. **Unit Tests**
   - Test ID shortening
   - Test format-specific escaping
   - Test option handling
   - Test error cases

2. **Integration Tests**
   - Test full graph exports
   - Verify format compliance
   - Test file I/O
   - Test large graphs

3. **Format Validation**
   - Validate against format specs
   - Test with format-specific tools
   - Verify readability
   - Check edge cases

## Next Steps

1. Implement DOT format exporter
2. Create base classes for common functionality
3. Add format-specific validation
4. Implement remaining formats
5. Add comprehensive tests
6. Create usage documentation