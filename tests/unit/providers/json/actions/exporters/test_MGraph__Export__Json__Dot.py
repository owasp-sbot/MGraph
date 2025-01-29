from unittest                                                              import TestCase
from osbot_utils.utils.Json import json_loads, json__equals__list_and_set
from mgraph_ai.providers.json.MGraph__Json                                 import MGraph__Json
from mgraph_ai.providers.json.actions.exporters.MGraph__Export__Json__Dot  import MGraph__Export__Json__Dot
from mgraph_ai.providers.json.actions.exporters.MGraph__Json__Export__Base import Export__Json__Node_Type, \
    Export__Json__Relation_Type


class test_MGraph__Export__Json__Dot(TestCase):

    def setUp(self):                                                           # Initialize test data
        self.mgraph = MGraph__Json()
        self.exporter = MGraph__Export__Json__Dot(self.mgraph.graph)
        self.test_data = { "string" : "value"         ,
                           "number" : 42              ,
                           "boolean": True            ,
                           "null"   : None            ,
                           "array"  : [1, 2, 3]       ,
                           "object" : {"key": "value"}}

    def test_node_style(self):                                                # Test node style generation
        styles = {
            Export__Json__Node_Type.OBJECT: self.exporter.get_node_style(Export__Json__Node_Type.OBJECT),
            Export__Json__Node_Type.ARRAY: self.exporter.get_node_style(Export__Json__Node_Type.ARRAY),
            Export__Json__Node_Type.VALUE: self.exporter.get_node_style(Export__Json__Node_Type.VALUE),
            Export__Json__Node_Type.PROPERTY: self.exporter.get_node_style(Export__Json__Node_Type.PROPERTY)
        }

        for style in styles.values():
            assert 'shape'                             in style
            assert 'style'                             in style
            assert 'fillcolor'                         in style

        assert styles[Export__Json__Node_Type.OBJECT]['shape']      == 'record'
        assert styles[Export__Json__Node_Type.VALUE]['shape']       == 'box'
        assert styles[Export__Json__Node_Type.PROPERTY]['shape']    == 'ellipse'

    def test_format_node_attributes(self):                                    # Test attribute formatting
        attrs = {
            'shape': 'box',
            'style': 'filled',
            'fillcolor': 'red',
            'label': 'test'
        }
        formatted = self.exporter.format_node_attributes(attrs)

        assert formatted.startswith(' [')
        assert formatted.endswith(']')
        assert 'shape="box"'                           in formatted
        assert 'style="filled"'                        in formatted
        assert 'fillcolor="red"'                       in formatted
        assert 'label="test"'                          in formatted

        assert self.exporter.format_node_attributes({}) == ""

    def test_simple_value_export(self):                                       # Test value node export
        self.mgraph.load().from_data("test_value")
        dot = self.exporter.to_string()
        assert dot == """\
digraph {
  // Graph settings
  graph [rankdir=LR]
  node [fontname="Arial"]
  edge [fontname="Arial"]

  // Nodes
  "value_0" [shape="box", style="filled", fillcolor="lightyellow", label="test_value"]

  // Edges
}"""

    def test_array_export(self):                                             # Test array node export
        test_array = [1, 2, "three"]
        self.mgraph.load().from_data(test_array)
        dot = self.exporter.to_string()
        assert dot == """\
digraph {
  // Graph settings
  graph [rankdir=LR]
  node [fontname="Arial"]
  edge [fontname="Arial"]

  // Nodes
  "array_0" [shape="record", style="filled", fillcolor="lightpink", label="array"]
  "value_0" [shape="box", style="filled", fillcolor="lightyellow", label="1"]
  "value_1" [shape="box", style="filled", fillcolor="lightyellow", label="2"]
  "value_2" [shape="box", style="filled", fillcolor="lightyellow", label="three"]

  // Edges
  "array_0" -> "value_0" [label="array_item"]
  "array_0" -> "value_1" [label="array_item"]
  "array_0" -> "value_2" [label="array_item"]
}"""



    def test_object_export(self):                                            # Test object node export
        test_obj = {"key1": "value1", "key2": 42}
        self.mgraph.load().from_data(test_obj)
        dot = self.exporter.to_string()
        assert dot == """\
digraph {
  // Graph settings
  graph [rankdir=LR]
  node [fontname="Arial"]
  edge [fontname="Arial"]

  // Nodes
  "object_0" [shape="record", style="filled", fillcolor="lightblue", label="object"]
  "property_0" [shape="ellipse", style="filled", fillcolor="lightgreen", label="key1"]
  "value_0" [shape="box", style="filled", fillcolor="lightyellow", label="value1"]
  "property_1" [shape="ellipse", style="filled", fillcolor="lightgreen", label="key2"]
  "value_1" [shape="box", style="filled", fillcolor="lightyellow", label="42"]

  // Edges
  "object_0" -> "property_0" [label="has_property"]
  "property_0" -> "value_0" [label="has_value"]
  "object_0" -> "property_1" [label="has_property"]
  "property_1" -> "value_1" [label="has_value"]
}"""

    def test_complex_structure(self):                                         # Test complex nested structure
        self.mgraph.load().from_data(self.test_data)
        dot = self.exporter.to_string()

        # Basic structure checks
        assert 'digraph {'                             in dot
        assert 'graph [rankdir=LR]'                    in dot
        assert 'node [fontname="Arial"]'               in dot
        assert 'edge [fontname="Arial"]'               in dot

        # Value types
        assert '"value"'                               in dot
        assert '"42"'                                  in dot
        assert '"true"'                                in dot
        assert '"null"'                                in dot

        # Node types
        assert 'object_'                               in dot
        assert 'array_'                                in dot
        assert 'value_'                                in dot
        assert 'property_'                             in dot

        # Relationship types
        assert Export__Json__Relation_Type.HAS_PROPERTY in dot
        assert Export__Json__Relation_Type.HAS_VALUE   in dot
        assert Export__Json__Relation_Type.ARRAY_ITEM  in dot

    def test_visual_attributes(self):                                         # Test visual styling
        self.mgraph.load().from_data(self.test_data)
        dot = self.exporter.to_string()

        # Style attributes
        assert 'shape='                                in dot
        assert 'style="filled"'                        in dot
        assert 'fillcolor='                            in dot

        # Layout directives
        assert 'rankdir=LR'                            in dot
        assert 'fontname="Arial"'                      in dot

    def test_empty_export(self):                                             # Test empty graph export
        dot = self.exporter.to_string()
        assert dot                                     == ""

    def test_nested_structure(self):                                         # Test deeply nested structure
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
        assert json__equals__list_and_set(json_loads(self.mgraph.export().to_string()),  nested_data)     # BUG
        dot = self.exporter.to_string()
        assert dot == """\
digraph {
  // Graph settings
  graph [rankdir=LR]
  node [fontname="Arial"]
  edge [fontname="Arial"]

  // Nodes
  "object_0" [shape="record", style="filled", fillcolor="lightblue", label="object"]
  "property_0" [shape="ellipse", style="filled", fillcolor="lightgreen", label="level1"]
  "object_1" [shape="record", style="filled", fillcolor="lightblue", label="object"]
  "property_1" [shape="ellipse", style="filled", fillcolor="lightgreen", label="level2"]
  "object_2" [shape="record", style="filled", fillcolor="lightblue", label="object"]
  "property_2" [shape="ellipse", style="filled", fillcolor="lightgreen", label="level3"]
  "object_3" [shape="record", style="filled", fillcolor="lightblue", label="object"]
  "property_3" [shape="ellipse", style="filled", fillcolor="lightgreen", label="arrayAAA"]
  "array_0" [shape="record", style="filled", fillcolor="lightpink", label="array"]
  "value_0" [shape="box", style="filled", fillcolor="lightyellow", label="1"]
  "object_4" [shape="record", style="filled", fillcolor="lightblue", label="object"]
  "property_4" [shape="ellipse", style="filled", fillcolor="lightgreen", label="nested"]
  "value_1" [shape="box", style="filled", fillcolor="lightyellow", label="value"]
  "array_1" [shape="record", style="filled", fillcolor="lightpink", label="array"]
  "value_2" [shape="box", style="filled", fillcolor="lightyellow", label="2"]
  "value_3" [shape="box", style="filled", fillcolor="lightyellow", label="3"]
  "property_5" [shape="ellipse", style="filled", fillcolor="lightgreen", label="valueBBB"]
  "value_4" [shape="box", style="filled", fillcolor="lightyellow", label="nested"]

  // Edges
  "object_0" -> "property_0" [label="has_property"]
  "object_1" -> "property_1" [label="has_property"]
  "object_2" -> "property_2" [label="has_property"]
  "object_3" -> "property_3" [label="has_property"]
  "array_0" -> "value_0" [label="array_item"]
  "object_4" -> "property_4" [label="has_property"]
  "property_4" -> "value_1" [label="has_value"]
  "array_0" -> "object_4" [label="array_item"]
  "array_1" -> "value_2" [label="array_item"]
  "array_1" -> "value_3" [label="array_item"]
  "array_0" -> "array_1" [label="array_item"]
  "property_3" -> "array_0" [label="has_value"]
  "object_3" -> "property_5" [label="has_property"]
  "property_5" -> "value_4" [label="has_value"]
  "property_2" -> "object_3" [label="has_value"]
  "property_1" -> "object_2" [label="has_value"]
  "property_0" -> "object_1" [label="has_value"]
}"""

    def test_dot_syntax(self):                                               # Test valid DOT syntax elements
        self.mgraph.load().from_data(self.test_data)
        dot = self.exporter.to_string()

        # Basic DOT syntax elements
        assert dot.startswith('digraph {')
        assert dot.endswith('}')
        assert '->'                                    in dot  # Edge operator
        assert '['                                     in dot  # Attribute start
        assert ']'                                     in dot  # Attribute end
        assert '"'                                     in dot  # String delimiter

        assert dot == """\
digraph {
  // Graph settings
  graph [rankdir=LR]
  node [fontname="Arial"]
  edge [fontname="Arial"]

  // Nodes
  "object_0" [shape="record", style="filled", fillcolor="lightblue", label="object"]
  "property_0" [shape="ellipse", style="filled", fillcolor="lightgreen", label="string"]
  "value_0" [shape="box", style="filled", fillcolor="lightyellow", label="value"]
  "property_1" [shape="ellipse", style="filled", fillcolor="lightgreen", label="number"]
  "value_1" [shape="box", style="filled", fillcolor="lightyellow", label="42"]
  "property_2" [shape="ellipse", style="filled", fillcolor="lightgreen", label="boolean"]
  "value_2" [shape="box", style="filled", fillcolor="lightyellow", label="true"]
  "property_3" [shape="ellipse", style="filled", fillcolor="lightgreen", label="null"]
  "value_3" [shape="box", style="filled", fillcolor="lightyellow", label="null"]
  "property_4" [shape="ellipse", style="filled", fillcolor="lightgreen", label="array"]
  "array_0" [shape="record", style="filled", fillcolor="lightpink", label="array"]
  "value_4" [shape="box", style="filled", fillcolor="lightyellow", label="1"]
  "value_5" [shape="box", style="filled", fillcolor="lightyellow", label="2"]
  "value_6" [shape="box", style="filled", fillcolor="lightyellow", label="3"]
  "property_5" [shape="ellipse", style="filled", fillcolor="lightgreen", label="object"]
  "object_1" [shape="record", style="filled", fillcolor="lightblue", label="object"]
  "property_6" [shape="ellipse", style="filled", fillcolor="lightgreen", label="key"]
  "value_7" [shape="box", style="filled", fillcolor="lightyellow", label="value"]

  // Edges
  "object_0" -> "property_0" [label="has_property"]
  "property_0" -> "value_0" [label="has_value"]
  "object_0" -> "property_1" [label="has_property"]
  "property_1" -> "value_1" [label="has_value"]
  "object_0" -> "property_2" [label="has_property"]
  "property_2" -> "value_2" [label="has_value"]
  "object_0" -> "property_3" [label="has_property"]
  "property_3" -> "value_3" [label="has_value"]
  "object_0" -> "property_4" [label="has_property"]
  "array_0" -> "value_4" [label="array_item"]
  "array_0" -> "value_5" [label="array_item"]
  "array_0" -> "value_6" [label="array_item"]
  "property_4" -> "array_0" [label="has_value"]
  "object_0" -> "property_5" [label="has_property"]
  "object_1" -> "property_6" [label="has_property"]
  "property_6" -> "value_7" [label="has_value"]
  "property_5" -> "object_1" [label="has_value"]
}"""