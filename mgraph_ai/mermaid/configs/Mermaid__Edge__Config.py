from osbot_utils.base_classes.Type_Safe import Type_Safe

class Mermaid__Edge__Config(Type_Safe):
    edge_mode        : str
    output_node_from : bool = False
    output_node_to   : bool = False