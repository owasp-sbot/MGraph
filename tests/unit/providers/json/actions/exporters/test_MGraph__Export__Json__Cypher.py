from unittest                                                                  import TestCase
from osbot_utils.utils.Json                                                    import json_loads
from mgraph_ai.providers.json.MGraph__Json                                     import MGraph__Json
from mgraph_ai.providers.json.actions.exporters.MGraph__Export__Json__Cypher   import MGraph__Export__Json__Cypher
from mgraph_ai.providers.json.actions.exporters.MGraph__Json__Export__Base     import Export__Json__Node_Type, Export__Json__Relation_Type


class test_MGraph__Export__Json__Cypher(TestCase):

    def setUp(self):                                                                               # Initialize test data
        self.mgraph    = MGraph__Json()
        self.exporter  = MGraph__Export__Json__Cypher(self.mgraph.graph)
        self.test_data = { "string" : "value"         ,
                           "number" : 42                ,
                           "boolean": True              ,
                           "null"   : None              ,
                           "array"  : [1, 2, 3]         ,
                           "object" : {"key": "value"}}

    def test_node_labels(self):                                                                    # Test node label generation
        labels = {
            Export__Json__Node_Type.OBJECT  : self.exporter.get_node_labels(Export__Json__Node_Type.OBJECT  ),
            Export__Json__Node_Type.ARRAY   : self.exporter.get_node_labels(Export__Json__Node_Type.ARRAY   ),
            Export__Json__Node_Type.VALUE   : self.exporter.get_node_labels(Export__Json__Node_Type.VALUE   ),
            Export__Json__Node_Type.PROPERTY: self.exporter.get_node_labels(Export__Json__Node_Type.PROPERTY)
        }

        assert labels[Export__Json__Node_Type.OBJECT  ] == 'JsonObject'
        assert labels[Export__Json__Node_Type.ARRAY   ] == 'JsonArray'
        assert labels[Export__Json__Node_Type.VALUE   ] == 'JsonValue'
        assert labels[Export__Json__Node_Type.PROPERTY] == 'JsonProperty'

    def test_value_formatting(self):                                                               # Test value formatting
        assert self.exporter.format_value(None)                  == "null"
        assert self.exporter.format_value(True)                  == "true"
        assert self.exporter.format_value(False)                 == "false"
        assert self.exporter.format_value(42)                    == "42"
        assert self.exporter.format_value(3.14)                  == "3.14"
        assert self.exporter.format_value("test")               == "'test'"
        assert self.exporter.format_value("test's")             == "'test\\'s'"
        assert self.exporter.format_value('test"s')             == "'test\\\"s'"

    def test_simple_value_export(self):                                                            # Test value node export
        self.mgraph.load().from_data("test_value")
        cypher = self.exporter.to_string()
        assert cypher == """\
// Clear existing data
MATCH (n) DETACH DELETE n;

// Create nodes
CREATE (:JsonValue  { value: 'test_value', valueType: 'str', id: 'value_0' });

// Create relationships"""

    def test_array_export(self):                                                                   # Test array node export
        test_array = [1, 2, "three"]
        self.mgraph.load().from_data(test_array)
        cypher = self.exporter.to_string()

        assert cypher == """\
// Clear existing data
MATCH (n) DETACH DELETE n;

// Create nodes
CREATE (:JsonArray  { type: 'array', id: 'array_0' });
CREATE (:JsonValue  { value: 1, valueType: 'int', id: 'value_0' });
CREATE (:JsonValue  { value: 2, valueType: 'int', id: 'value_1' });
CREATE (:JsonValue  { value: 'three', valueType: 'str', id: 'value_2' });

// Create relationships
MATCH (from { id: 'array_0' }), (to { id: 'value_0' }) CREATE (from)-[:array_item { index: 0 }]->(to);
MATCH (from { id: 'array_0' }), (to { id: 'value_1' }) CREATE (from)-[:array_item { index: 1 }]->(to);
MATCH (from { id: 'array_0' }), (to { id: 'value_2' }) CREATE (from)-[:array_item { index: 2 }]->(to);"""

    def test_object_export(self):                                                                  # Test object node export
        test_obj = {"key1": "value1", "key2": 42}
        self.mgraph.load().from_data(test_obj)
        cypher = self.exporter.to_string()
        assert cypher == """\
// Clear existing data
MATCH (n) DETACH DELETE n;

// Create nodes
CREATE (:JsonObject  { type: 'object', id: 'object_0' });
CREATE (:JsonProperty  { name: 'key1', id: 'property_0' });
CREATE (:JsonValue  { value: 'value1', valueType: 'str', id: 'value_0' });
CREATE (:JsonProperty  { name: 'key2', id: 'property_1' });
CREATE (:JsonValue  { value: 42, valueType: 'int', id: 'value_1' });

// Create relationships
MATCH (from { id: 'object_0' }), (to { id: 'property_0' }) CREATE (from)-[:has_property]->(to);
MATCH (from { id: 'property_0' }), (to { id: 'value_0' }) CREATE (from)-[:has_value]->(to);
MATCH (from { id: 'object_0' }), (to { id: 'property_1' }) CREATE (from)-[:has_property]->(to);
MATCH (from { id: 'property_1' }), (to { id: 'value_1' }) CREATE (from)-[:has_value]->(to);"""

    def test_complex_structure(self):                                                              # Test complex nested structure
        self.mgraph.load().from_data(self.test_data)
        cypher = self.exporter.to_string()

        # Check node types
        assert "JsonObject"                             in cypher
        assert "JsonArray"                              in cypher
        assert "JsonValue"                              in cypher
        assert "JsonProperty"                           in cypher

        # Check relationship types
        assert Export__Json__Relation_Type.HAS_PROPERTY in cypher
        assert Export__Json__Relation_Type.HAS_VALUE    in cypher
        assert Export__Json__Relation_Type.ARRAY_ITEM   in cypher

        # Check value types
        assert "valueType: 'str'"                       in cypher
        assert "valueType: 'int'"                       in cypher
        assert "valueType: 'bool'"                      in cypher
        assert "valueType: 'null'"                      in cypher

    def test_nested_structure(self):                                                               # Test deeply nested structure
        nested_data = {
            "level1": {
                "level2": {
                    "level3": {
                        "arrayAAA": [1, {"nested": "value"}, [2, 3]],
                        "valueBBB": "nested"
                    }
                }
            }
        }
        self.mgraph.load().from_data(nested_data)
        cypher_text = self.exporter.to_string()
        assert cypher_text == """\
// Clear existing data
MATCH (n) DETACH DELETE n;

// Create nodes
CREATE (:JsonObject  { type: 'object', id: 'object_0' });
CREATE (:JsonProperty  { name: 'level1', id: 'property_0' });
CREATE (:JsonObject  { type: 'object', id: 'object_1' });
CREATE (:JsonProperty  { name: 'level2', id: 'property_1' });
CREATE (:JsonObject  { type: 'object', id: 'object_2' });
CREATE (:JsonProperty  { name: 'level3', id: 'property_2' });
CREATE (:JsonObject  { type: 'object', id: 'object_3' });
CREATE (:JsonProperty  { name: 'arrayAAA', id: 'property_3' });
CREATE (:JsonArray  { type: 'array', id: 'array_0' });
CREATE (:JsonValue  { value: 1, valueType: 'int', id: 'value_0' });
CREATE (:JsonObject  { type: 'object', id: 'object_4' });
CREATE (:JsonProperty  { name: 'nested', id: 'property_4' });
CREATE (:JsonValue  { value: 'value', valueType: 'str', id: 'value_1' });
CREATE (:JsonArray  { type: 'array', id: 'array_1' });
CREATE (:JsonValue  { value: 2, valueType: 'int', id: 'value_2' });
CREATE (:JsonValue  { value: 3, valueType: 'int', id: 'value_3' });
CREATE (:JsonProperty  { name: 'valueBBB', id: 'property_5' });
CREATE (:JsonValue  { value: 'nested', valueType: 'str', id: 'value_4' });

// Create relationships
MATCH (from { id: 'object_0' }), (to { id: 'property_0' }) CREATE (from)-[:has_property]->(to);
MATCH (from { id: 'object_1' }), (to { id: 'property_1' }) CREATE (from)-[:has_property]->(to);
MATCH (from { id: 'object_2' }), (to { id: 'property_2' }) CREATE (from)-[:has_property]->(to);
MATCH (from { id: 'object_3' }), (to { id: 'property_3' }) CREATE (from)-[:has_property]->(to);
MATCH (from { id: 'array_0' }), (to { id: 'value_0' }) CREATE (from)-[:array_item { index: 0 }]->(to);
MATCH (from { id: 'object_4' }), (to { id: 'property_4' }) CREATE (from)-[:has_property]->(to);
MATCH (from { id: 'property_4' }), (to { id: 'value_1' }) CREATE (from)-[:has_value]->(to);
MATCH (from { id: 'array_0' }), (to { id: 'object_4' }) CREATE (from)-[:array_item { index: 1 }]->(to);
MATCH (from { id: 'array_1' }), (to { id: 'value_2' }) CREATE (from)-[:array_item { index: 0 }]->(to);
MATCH (from { id: 'array_1' }), (to { id: 'value_3' }) CREATE (from)-[:array_item { index: 1 }]->(to);
MATCH (from { id: 'array_0' }), (to { id: 'array_1' }) CREATE (from)-[:array_item { index: 2 }]->(to);
MATCH (from { id: 'property_3' }), (to { id: 'array_0' }) CREATE (from)-[:has_value]->(to);
MATCH (from { id: 'object_3' }), (to { id: 'property_5' }) CREATE (from)-[:has_property]->(to);
MATCH (from { id: 'property_5' }), (to { id: 'value_4' }) CREATE (from)-[:has_value]->(to);
MATCH (from { id: 'property_2' }), (to { id: 'object_3' }) CREATE (from)-[:has_value]->(to);
MATCH (from { id: 'property_1' }), (to { id: 'object_2' }) CREATE (from)-[:has_value]->(to);
MATCH (from { id: 'property_0' }), (to { id: 'object_1' }) CREATE (from)-[:has_value]->(to);"""

    def test_cypher_syntax(self):                                                                  # Test valid Cypher syntax elements
        self.mgraph.load().from_data(self.test_data)
        cypher = self.exporter.to_string()
        assert cypher == """\
// Clear existing data
MATCH (n) DETACH DELETE n;

// Create nodes
CREATE (:JsonObject  { type: 'object', id: 'object_0' });
CREATE (:JsonProperty  { name: 'string', id: 'property_0' });
CREATE (:JsonValue  { value: 'value', valueType: 'str', id: 'value_0' });
CREATE (:JsonProperty  { name: 'number', id: 'property_1' });
CREATE (:JsonValue  { value: 42, valueType: 'int', id: 'value_1' });
CREATE (:JsonProperty  { name: 'boolean', id: 'property_2' });
CREATE (:JsonValue  { value: true, valueType: 'bool', id: 'value_2' });
CREATE (:JsonProperty  { name: 'null', id: 'property_3' });
CREATE (:JsonValue  { value: null, valueType: 'null', id: 'value_3' });
CREATE (:JsonProperty  { name: 'array', id: 'property_4' });
CREATE (:JsonArray  { type: 'array', id: 'array_0' });
CREATE (:JsonValue  { value: 1, valueType: 'int', id: 'value_4' });
CREATE (:JsonValue  { value: 2, valueType: 'int', id: 'value_5' });
CREATE (:JsonValue  { value: 3, valueType: 'int', id: 'value_6' });
CREATE (:JsonProperty  { name: 'object', id: 'property_5' });
CREATE (:JsonObject  { type: 'object', id: 'object_1' });
CREATE (:JsonProperty  { name: 'key', id: 'property_6' });
CREATE (:JsonValue  { value: 'value', valueType: 'str', id: 'value_7' });

// Create relationships
MATCH (from { id: 'object_0' }), (to { id: 'property_0' }) CREATE (from)-[:has_property]->(to);
MATCH (from { id: 'property_0' }), (to { id: 'value_0' }) CREATE (from)-[:has_value]->(to);
MATCH (from { id: 'object_0' }), (to { id: 'property_1' }) CREATE (from)-[:has_property]->(to);
MATCH (from { id: 'property_1' }), (to { id: 'value_1' }) CREATE (from)-[:has_value]->(to);
MATCH (from { id: 'object_0' }), (to { id: 'property_2' }) CREATE (from)-[:has_property]->(to);
MATCH (from { id: 'property_2' }), (to { id: 'value_2' }) CREATE (from)-[:has_value]->(to);
MATCH (from { id: 'object_0' }), (to { id: 'property_3' }) CREATE (from)-[:has_property]->(to);
MATCH (from { id: 'property_3' }), (to { id: 'value_3' }) CREATE (from)-[:has_value]->(to);
MATCH (from { id: 'object_0' }), (to { id: 'property_4' }) CREATE (from)-[:has_property]->(to);
MATCH (from { id: 'array_0' }), (to { id: 'value_4' }) CREATE (from)-[:array_item { index: 0 }]->(to);
MATCH (from { id: 'array_0' }), (to { id: 'value_5' }) CREATE (from)-[:array_item { index: 1 }]->(to);
MATCH (from { id: 'array_0' }), (to { id: 'value_6' }) CREATE (from)-[:array_item { index: 2 }]->(to);
MATCH (from { id: 'property_4' }), (to { id: 'array_0' }) CREATE (from)-[:has_value]->(to);
MATCH (from { id: 'object_0' }), (to { id: 'property_5' }) CREATE (from)-[:has_property]->(to);
MATCH (from { id: 'object_1' }), (to { id: 'property_6' }) CREATE (from)-[:has_property]->(to);
MATCH (from { id: 'property_6' }), (to { id: 'value_7' }) CREATE (from)-[:has_value]->(to);
MATCH (from { id: 'property_5' }), (to { id: 'object_1' }) CREATE (from)-[:has_value]->(to);"""

    def test_empty_export(self):                                                                   # Test empty graph export
        cypher = self.exporter.to_string()
        assert cypher                                   == ""

    def test_special_characters(self):                                                             # Test handling of special characters
        special_data = {
            "quotes": "Single ' and Double \" quotes",
            "newlines": "Line 1\nLine 2",
            "backslash": "Contains \\ backslash"
        }
        self.mgraph.load().from_data(special_data)
        cypher = self.exporter.to_string()

        assert "Single \\\' and Double \\\" quotes"     in cypher                               # todo: double check that this is working as expected
        assert "Line 1\nLine 2"                         in cypher
        assert "Contains \\ backslash"                  in cypher