# from https://mermaid.js.org/syntax/flowchart.html
class Mermain_Examples__FlowChart:
    example_1__a_node_default = """
flowchart LR
    id
    """
    example_2__a_node_with_text = """
flowchart LR
    id1[This is the text in the box]    
    """

    example_3__a_node_with_unicode_text = """
flowchart LR
    id["This ❤ Unicode"]    
    """
    example_4__a_node_with_markdown_formatting = """
%%{init: {"flowchart": {"htmlLabels": false}} }%%
flowchart LR
    markdown["`This **is** _Markdown_`"]
    newLines["`Line1
    Line 2
    Line 3`"]
    markdown --> newLines 
    """

    example_5__direction__from_top_to_bottom  = """
flowchart TD
    Start --> Stop    
    """

    example_6__direction__from_left_to_right  = """
flowchart LR
    Start --> Stop    
    """
    example_7__node_shapes_a_node_with_round_edges  = """
flowchart LR
    id1(This is the text in the box)
    """

    example_8__node_shapes_a_stadium_shaped_node  = """
flowchart LR
    id1([This is the text in the box])
    """

    example_9__node_shapes_a_node_in_a_subroutine ="""
flowchart LR
    id1[[This is the text in the box]]
    """

    example_10__node_shapes_a_node_in_a_cylindrical_shape ="""
flowchart LR
    id1[(Database)]
    """

    example_11__node_shapes_a_node_in_the_form_of_a_circle = """
flowchart LR
    id1((This is the text in the circle))
    """

    example_12__node_shapes_a_node_in_an_asymmetric_shape = """
flowchart LR
    id1>This is the text in the box]
    """

    example_13__node_shapes_a_node_rhombus = """
flowchart LR
    id1{This is the text in the box}
    """

    example_14__node_shapes_a_hexagon_node = """
flowchart LR
    id1{{This is the text in the box}}
    """

    example_15__node_shapes_parallelogram = """
flowchart TD
    id1[/This is the text in the box/]
    """

    example_16__node_shapes_parallelogram_alt = r"""
flowchart TD
    id1[\This is the text in the box\]
    """

    example_17__node_shapes_trapezoid = r"""
flowchart TD
    A[/Christmas\]
    """

    example_18__node_shapes_trapezoid_alt = r"""
flowchart TD
    B[\Go shopping/]
    """

    example_19__node_shapes_double_circle = """
flowchart TD
    id1(((This is the text in the circle)))
    """