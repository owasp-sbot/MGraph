from unittest                                               import TestCase
from mgraph_ai.mermaid.schemas.Schema__Mermaid__Node__Shape import Schema__Mermaid__Node__Shape


class test_Schema__Mermaid__Node__Shape(TestCase):

    def test_get_shape_with_enum(self):
        assert Schema__Mermaid__Node__Shape.get_shape(Schema__Mermaid__Node__Shape.default    ) ==  Schema__Mermaid__Node__Shape.default
        assert Schema__Mermaid__Node__Shape.get_shape(Schema__Mermaid__Node__Shape.round_edges) ==  Schema__Mermaid__Node__Shape.round_edges
        assert Schema__Mermaid__Node__Shape.get_shape(Schema__Mermaid__Node__Shape.circle     ) ==  Schema__Mermaid__Node__Shape.circle
        assert Schema__Mermaid__Node__Shape.get_shape(Schema__Mermaid__Node__Shape.rhombus    ) ==  Schema__Mermaid__Node__Shape.rhombus

    def test_get_shape_with_string(self):
        assert Schema__Mermaid__Node__Shape.get_shape('rhombus'    ) ==  Schema__Mermaid__Node__Shape.rhombus
        assert Schema__Mermaid__Node__Shape.get_shape('circle'     ) ==  Schema__Mermaid__Node__Shape.circle
        assert Schema__Mermaid__Node__Shape.get_shape('default'    ) ==  Schema__Mermaid__Node__Shape.default
        assert Schema__Mermaid__Node__Shape.get_shape('round_edges') ==  Schema__Mermaid__Node__Shape.round_edges


    def test_get_shape_with_non_string_non_enum(self):
        self.assertEqual(Schema__Mermaid__Node__Shape.get_shape(123  ), Schema__Mermaid__Node__Shape.default)
        self.assertEqual(Schema__Mermaid__Node__Shape.get_shape('aaa'), Schema__Mermaid__Node__Shape.default)
        self.assertEqual(Schema__Mermaid__Node__Shape.get_shape(None ), Schema__Mermaid__Node__Shape.default)

    def test_enum_values(self):
        assert Schema__Mermaid__Node__Shape.default.value           == ('['  ,  ']'  )
        assert Schema__Mermaid__Node__Shape.round_edges.value       == ('('  ,  ')'  )
        assert Schema__Mermaid__Node__Shape.circle.value            == ('((' ,  '))' )
        assert Schema__Mermaid__Node__Shape.hexagon.value           == ('{{' ,  '}}' )
        assert Schema__Mermaid__Node__Shape.parallelogram.value     == ('[/' ,  '/]' )
        assert Schema__Mermaid__Node__Shape.parallelogram_alt.value == ('[\\',  '\\]')
        assert Schema__Mermaid__Node__Shape.rectangle.value         == ('['  ,  ']'  )
        assert Schema__Mermaid__Node__Shape.trapezoid.value         == ('[/' , r'\]' )
        assert Schema__Mermaid__Node__Shape.trapezoid_alt.value     == ('[\\',  '/]' )