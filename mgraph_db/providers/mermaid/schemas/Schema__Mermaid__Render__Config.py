from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Diagram_Direction import Schema__Mermaid__Diagram__Direction
from mgraph_db.providers.mermaid.schemas.Schema__Mermaid__Diagram__Type     import Schema__Mermaid__Diagram__Type
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe

class Schema__Mermaid__Render__Config(Type_Safe):
    add_nodes         : bool = True
    diagram_direction : Schema__Mermaid__Diagram__Direction = Schema__Mermaid__Diagram__Direction.LR
    diagram_type      : Schema__Mermaid__Diagram__Type      = Schema__Mermaid__Diagram__Type.graph
    directives        : list
    line_before_edges : bool = True