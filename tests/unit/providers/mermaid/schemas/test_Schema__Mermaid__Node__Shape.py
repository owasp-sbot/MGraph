from unittest                                                            import TestCase
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Node__Shape   import Schema__Mermaid__Node__Shape



class test_Schema__Mermaid__Node__Shape(TestCase):

    def test_shape_values(self):                                                    # Tests shape values and format
        assert Schema__Mermaid__Node__Shape.default.value         == ('['  , ']'  )
        assert Schema__Mermaid__Node__Shape.circle.value          == ('((' , '))' )
        assert Schema__Mermaid__Node__Shape.rhombus.value         == ('{'  , '}'  )
        assert Schema__Mermaid__Node__Shape.round_edges.value     == ('('  , ')'  )

    def test_get_shape(self):                                                       # Tests shape retrieval method
        # Test with enum value
        shape = Schema__Mermaid__Node__Shape.circle
        assert Schema__Mermaid__Node__Shape.get_shape(shape) == shape

        # Test with string value
        assert Schema__Mermaid__Node__Shape.get_shape('circle') == Schema__Mermaid__Node__Shape.circle

        # Test with invalid value
        assert Schema__Mermaid__Node__Shape.get_shape('invalid') == Schema__Mermaid__Node__Shape.default
        assert Schema__Mermaid__Node__Shape.get_shape(None) == Schema__Mermaid__Node__Shape.default

    def test_shape_uniqueness(self):                                                # Tests that all shapes have unique values
        shape_values = [shape.value for shape in Schema__Mermaid__Node__Shape]
        assert len(shape_values) == len(set(shape_values))  # All values should be unique