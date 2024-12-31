from unittest import TestCase

from mgraph_ai.mermaid.models.Mermaid__Node__Shape import Mermaid__Node__Shape


class test_Mermaid__Node__Shape(TestCase):

    def test_get_shape_with_enum(self):
        assert Mermaid__Node__Shape.get_shape(Mermaid__Node__Shape.default    ) ==  Mermaid__Node__Shape.default
        assert Mermaid__Node__Shape.get_shape(Mermaid__Node__Shape.round_edges) ==  Mermaid__Node__Shape.round_edges
        assert Mermaid__Node__Shape.get_shape(Mermaid__Node__Shape.circle     ) ==  Mermaid__Node__Shape.circle
        assert Mermaid__Node__Shape.get_shape(Mermaid__Node__Shape.rhombus    ) ==  Mermaid__Node__Shape.rhombus

    def test_get_shape_with_string(self):
        assert Mermaid__Node__Shape.get_shape('rhombus'    ) ==  Mermaid__Node__Shape.rhombus
        assert Mermaid__Node__Shape.get_shape('circle'     ) ==  Mermaid__Node__Shape.circle
        assert Mermaid__Node__Shape.get_shape('default'    ) ==  Mermaid__Node__Shape.default
        assert Mermaid__Node__Shape.get_shape('round_edges') ==  Mermaid__Node__Shape.round_edges


    def test_get_shape_with_non_string_non_enum(self):
        self.assertEqual(Mermaid__Node__Shape.get_shape(123  ), Mermaid__Node__Shape.default)
        self.assertEqual(Mermaid__Node__Shape.get_shape('aaa'), Mermaid__Node__Shape.default)
        self.assertEqual(Mermaid__Node__Shape.get_shape(None ), Mermaid__Node__Shape.default)

    def test_enum_values(self):
        assert Mermaid__Node__Shape.default.value           == ('['  ,  ']'  )
        assert Mermaid__Node__Shape.round_edges.value       == ('('  ,  ')'  )
        assert Mermaid__Node__Shape.circle.value            == ('((' ,  '))' )
        assert Mermaid__Node__Shape.hexagon.value           == ('{{' ,  '}}' )
        assert Mermaid__Node__Shape.parallelogram.value     == ('[/' ,  '/]' )
        assert Mermaid__Node__Shape.parallelogram_alt.value == ('[\\',  '\\]')
        assert Mermaid__Node__Shape.rectangle.value         == ('['  ,  ']'  )
        assert Mermaid__Node__Shape.trapezoid.value         == ('[/' , r'\]' )
        assert Mermaid__Node__Shape.trapezoid_alt.value     == ('[\\',  '/]' )