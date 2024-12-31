from __future__ import annotations
from enum import Enum


class Mermaid__Node__Shape(Enum):
    asymmetric          = ('>'  ,  ']'  )        # Asymmetric
    circle              = ('((' ,  '))' )        # Circle, used for endpoints or start/end points
    cylindrical         = ('[(' ,  ')]' )        # Cylindrical
    default             = ('['  ,  ']'  )        # Rectangle
    double_circle       = ('(((',  ')))')        # Double Circle
    round_edges         = ('('  ,  ')'  )        # Stadium shape, used for processes or operations
    rhombus             = ('{'  ,  '}'  )        # Rhombus, often synonymous with diamond in diagramming contexts
    hexagon             = ('{{' ,  '}}' )        # Hexagon, used for preparation or complex processing
    parallelogram       = ('[/' ,  '/]' )        # Parallelogram, used for input/output
    parallelogram_alt   = ('[\\',  '\\]')        # Alternative parallelogram, also used for input/output
    rectangle           = ('['  ,  ']'  )        # Rectangle, used for process
    stadium             = ('([' ,  '])' )        # Stadium
    subroutine          = ('[[',   ']]' )        # Subroutine
    trapezoid           = ('[/' , r'\]' )        # Trapezoid, used for manual operations             # todo: figure out why this line is throwing the compile error of: SyntaxWarning: invalid escape sequence '\]'
    trapezoid_alt       = ('[\\',  '/]' )        # Inverted trapezoid, also used for manual operations

    @staticmethod
    def get_shape(value = None) -> Mermaid__Node__Shape:
        if isinstance(value, Mermaid__Node__Shape):
            return value
        if type(value) is str:
            for shape in Mermaid__Node__Shape:
                if value == shape.name:
                    return shape
        return Mermaid__Node__Shape.default