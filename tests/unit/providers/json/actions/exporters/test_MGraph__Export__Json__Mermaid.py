from unittest                                                                  import TestCase
from osbot_utils.utils.Json                                                    import json_loads
from mgraph_ai.providers.json.MGraph__Json                                     import MGraph__Json
from mgraph_ai.providers.json.actions.exporters.MGraph__Export__Json__Mermaid  import MGraph__Export__Json__Mermaid
from mgraph_ai.providers.json.actions.exporters.MGraph__Json__Export__Base     import Export__Json__Node_Type, Export__Json__Relation_Type


class test_MGraph__Export__Json__Mermaid(TestCase):

    def setUp(self):                                                                               # Initialize test data
        self.mgraph    = MGraph__Json()
        self.exporter  = MGraph__Export__Json__Mermaid(self.mgraph.graph)
        self.test_data = { "string" : "value"         ,
                           "number" : 42                ,
                           "boolean": True              ,
                           "null"   : None              ,
                           "array"  : [1, 2, 3]         ,
                           "object" : {"key": "value"}}

    def test_node_style(self):                                                                    # Test node style generation
        styles = {
            Export__Json__Node_Type.OBJECT  : self.exporter.get_node_style(Export__Json__Node_Type.OBJECT  ),
            Export__Json__Node_Type.ARRAY   : self.exporter.get_node_style(Export__Json__Node_Type.ARRAY   ),
            Export__Json__Node_Type.VALUE   : self.exporter.get_node_style(Export__Json__Node_Type.VALUE   ),
            Export__Json__Node_Type.PROPERTY: self.exporter.get_node_style(Export__Json__Node_Type.PROPERTY)
        }

        for style in styles.values():
            assert 'shape'                             in style
            assert 'style'                             in style
            assert 'fill'                              in style
            assert 'stroke'                            in style

        assert styles[Export__Json__Node_Type.OBJECT]['shape']      == 'rect'
        assert styles[Export__Json__Node_Type.VALUE]['shape']       == 'square'
        assert styles[Export__Json__Node_Type.PROPERTY]['shape']    == 'stadium'


    def test_simple_value_export(self):                                                           # Test value node export
        self.mgraph.load().from_data("test_value")
        mermaid = self.exporter.to_string()
        assert mermaid == """\
flowchart LR
    value_0[test_value]

    style value_0 fill:#FFF9C4,stroke:#FBC02D"""

    def test_array_export(self):                                                                  # Test array node export
        test_array = [1, 2, "three"]
        self.mgraph.load().from_data(test_array)
        mermaid = self.exporter.to_string()
        assert mermaid == """\
flowchart LR
    array_0[array]
    value_0[1]
    value_1[2]
    value_2[three]

    array_0 ==>|array_item| value_0
    array_0 ==>|array_item| value_1
    array_0 ==>|array_item| value_2

    style array_0 fill:#F8BBD0,stroke:#C2185B
    style value_0 fill:#FFF9C4,stroke:#FBC02D
    style value_1 fill:#FFF9C4,stroke:#FBC02D
    style value_2 fill:#FFF9C4,stroke:#FBC02D"""

    def test_object_export(self):                                                                 # Test object node export
        test_obj = {"key1": "value1", "key2": 42}
        self.mgraph.load().from_data(test_obj)
        mermaid = self.exporter.to_string()
        assert mermaid == """\
flowchart LR
    object_0[object]
    property_0[key1]
    value_0[value1]
    property_1[key2]
    value_1[42]

    object_0 -->|has_property| property_0
    property_0 -->|has_value| value_0
    object_0 -->|has_property| property_1
    property_1 -->|has_value| value_1

    style object_0 fill:#BBDEFB,stroke:#1976D2
    style property_0 fill:#C8E6C9,stroke:#388E3C
    style value_0 fill:#FFF9C4,stroke:#FBC02D
    style property_1 fill:#C8E6C9,stroke:#388E3C
    style value_1 fill:#FFF9C4,stroke:#FBC02D"""

    def test_complex_structure(self):                                                             # Test complex nested structure
        self.mgraph.load().from_data(self.test_data)
        mermaid = self.exporter.to_string()

        # Basic structure checks
        assert 'flowchart LR'                           in mermaid

        # Value types
        assert 'value'                                  in mermaid
        assert '42'                                     in mermaid
        assert 'true'                                   in mermaid
        assert 'null'                                   in mermaid

        # Node types
        assert 'object_'                                in mermaid
        assert 'array_'                                 in mermaid
        assert 'value_'                                 in mermaid
        assert 'property_'                              in mermaid

        # Relationship types
        assert Export__Json__Relation_Type.HAS_PROPERTY in mermaid
        assert Export__Json__Relation_Type.HAS_VALUE    in mermaid
        assert Export__Json__Relation_Type.ARRAY_ITEM   in mermaid

        # Style section at the end
        style_section = mermaid.split('\n\n')[-1]
        assert style_section.startswith('    style ')

    def test_visual_attributes(self):                                                             # Test visual styling
        self.mgraph.load().from_data(self.test_data)
        mermaid = self.exporter.to_string()

        # Style attributes
        assert 'fill:'                                  in mermaid
        assert 'stroke:'                                in mermaid

        # Verify styles are at the end
        sections = mermaid.split('\n\n')
        assert sections[-1].startswith('    style ')

    def test_empty_export(self):                                                                  # Test empty graph export
        mermaid = self.exporter.to_string()
        assert mermaid                                  == ""

    def test_nested_structure(self):                                                              # Test deeply nested structure
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
        assert json_loads(self.mgraph.export().to_string()) == nested_data
        mermaid = self.exporter.to_string()
        assert mermaid == """\
flowchart LR
    object_0[object]
    property_0[level1]
    object_1[object]
    property_1[level2]
    object_2[object]
    property_2[level3]
    object_3[object]
    property_3[arrayAAA]
    array_0[array]
    value_0[1]
    object_4[object]
    property_4[nested]
    value_1[value]
    array_1[array]
    value_2[2]
    value_3[3]
    property_5[valueBBB]
    value_4[nested]

    object_0 -->|has_property| property_0
    object_1 -->|has_property| property_1
    object_2 -->|has_property| property_2
    object_3 -->|has_property| property_3
    array_0 ==>|array_item| value_0
    object_4 -->|has_property| property_4
    property_4 -->|has_value| value_1
    array_0 ==>|array_item| object_4
    array_1 ==>|array_item| value_2
    array_1 ==>|array_item| value_3
    array_0 ==>|array_item| array_1
    property_3 -->|has_value| array_0
    object_3 -->|has_property| property_5
    property_5 -->|has_value| value_4
    property_2 -->|has_value| object_3
    property_1 -->|has_value| object_2
    property_0 -->|has_value| object_1

    style object_0 fill:#BBDEFB,stroke:#1976D2
    style property_0 fill:#C8E6C9,stroke:#388E3C
    style object_1 fill:#BBDEFB,stroke:#1976D2
    style property_1 fill:#C8E6C9,stroke:#388E3C
    style object_2 fill:#BBDEFB,stroke:#1976D2
    style property_2 fill:#C8E6C9,stroke:#388E3C
    style object_3 fill:#BBDEFB,stroke:#1976D2
    style property_3 fill:#C8E6C9,stroke:#388E3C
    style array_0 fill:#F8BBD0,stroke:#C2185B
    style value_0 fill:#FFF9C4,stroke:#FBC02D
    style object_4 fill:#BBDEFB,stroke:#1976D2
    style property_4 fill:#C8E6C9,stroke:#388E3C
    style value_1 fill:#FFF9C4,stroke:#FBC02D
    style array_1 fill:#F8BBD0,stroke:#C2185B
    style value_2 fill:#FFF9C4,stroke:#FBC02D
    style value_3 fill:#FFF9C4,stroke:#FBC02D
    style property_5 fill:#C8E6C9,stroke:#388E3C
    style value_4 fill:#FFF9C4,stroke:#FBC02D"""

    def test_mermaid_syntax(self):                                                               # Test valid Mermaid syntax elements
        self.mgraph.load().from_data(self.test_data)
        mermaid = self.exporter.to_string()

        # Basic Mermaid syntax elements
        assert mermaid.startswith('flowchart LR')       # Flowchart definition
        assert '-->'                                     in mermaid  # Arrow syntax
        assert '==>'                                     in mermaid  # Thick arrow
        assert '|'                                       in mermaid  # Label delimiter

        # Verify styles section is at the end
        sections = mermaid.split('\n\n')
        assert sections[-1].startswith('    style ')

        assert mermaid == """\
flowchart LR
    object_0[object]
    property_0[string]
    value_0[value]
    property_1[number]
    value_1[42]
    property_2[boolean]
    value_2[true]
    property_3[null]
    value_3[null]
    property_4[array]
    array_0[array]
    value_4[1]
    value_5[2]
    value_6[3]
    property_5[object]
    object_1[object]
    property_6[key]
    value_7[value]

    object_0 -->|has_property| property_0
    property_0 -->|has_value| value_0
    object_0 -->|has_property| property_1
    property_1 -->|has_value| value_1
    object_0 -->|has_property| property_2
    property_2 -->|has_value| value_2
    object_0 -->|has_property| property_3
    property_3 -->|has_value| value_3
    object_0 -->|has_property| property_4
    array_0 ==>|array_item| value_4
    array_0 ==>|array_item| value_5
    array_0 ==>|array_item| value_6
    property_4 -->|has_value| array_0
    object_0 -->|has_property| property_5
    object_1 -->|has_property| property_6
    property_6 -->|has_value| value_7
    property_5 -->|has_value| object_1

    style object_0 fill:#BBDEFB,stroke:#1976D2
    style property_0 fill:#C8E6C9,stroke:#388E3C
    style value_0 fill:#FFF9C4,stroke:#FBC02D
    style property_1 fill:#C8E6C9,stroke:#388E3C
    style value_1 fill:#FFF9C4,stroke:#FBC02D
    style property_2 fill:#C8E6C9,stroke:#388E3C
    style value_2 fill:#FFF9C4,stroke:#FBC02D
    style property_3 fill:#C8E6C9,stroke:#388E3C
    style value_3 fill:#FFF9C4,stroke:#FBC02D
    style property_4 fill:#C8E6C9,stroke:#388E3C
    style array_0 fill:#F8BBD0,stroke:#C2185B
    style value_4 fill:#FFF9C4,stroke:#FBC02D
    style value_5 fill:#FFF9C4,stroke:#FBC02D
    style value_6 fill:#FFF9C4,stroke:#FBC02D
    style property_5 fill:#C8E6C9,stroke:#388E3C
    style object_1 fill:#BBDEFB,stroke:#1976D2
    style property_6 fill:#C8E6C9,stroke:#388E3C
    style value_7 fill:#FFF9C4,stroke:#FBC02D"""