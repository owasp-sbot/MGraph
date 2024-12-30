from typing                             import Dict, Any
from osbot_utils.base_classes.Type_Safe import Type_Safe
from mgraph_ai.core.MGraph__Node        import MGraph__Node

class MGraph__Edge(Type_Safe):
    attributes : Dict[str, Any]
    from_node  : MGraph__Node
    to_node    : MGraph__Node

    def __str__(self):
        return f'[Graph Edge] from "{self.from_node.node_id}" to "{self.to_node.node_id}" '