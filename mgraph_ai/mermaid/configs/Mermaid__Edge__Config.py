from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self


class Mermaid__Edge__Config(Kwargs_To_Self):
    edge_mode        : str
    output_node_from : bool = False
    output_node_to   : bool = False