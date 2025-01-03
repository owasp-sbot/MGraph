from typing import Dict

from mgraph_ai.base.MGraph__Edge        import MGraph__Edge
from mgraph_ai.base.MGraph__Node        import MGraph__Node
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.helpers                import Random_Guid


class MGraph__Graph(Type_Safe):
    edges    : Dict[Random_Guid, MGraph__Edge]
    graph_id : Random_Guid
    nodes    : Dict[Random_Guid, MGraph__Node]