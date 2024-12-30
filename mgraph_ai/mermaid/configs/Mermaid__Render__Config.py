from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self


class Mermaid__Render__Config(Kwargs_To_Self):
    add_nodes         : bool = True
    directives        : list
    line_before_edges : bool = True