from typing                             import Dict, Any
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.helpers.Random_Guid    import Random_Guid

class MGraph__Edge(Type_Safe):
    attributes    : Dict[str, Any]
    from_node_id  : Random_Guid
    from_node_type: type
    to_node_id    : Random_Guid
    to_node_type  : type

    def __str__(self):
        return f'[Graph Edge] from "{self.from_node_id}" to "{self.to_node_id}" '