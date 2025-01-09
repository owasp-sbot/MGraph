from osbot_utils.type_safe.Type_Safe import Type_Safe


class Mermaid__Render__Config(Type_Safe):
    add_nodes         : bool = True
    directives        : list
    line_before_edges : bool = True