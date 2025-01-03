from typing                             import Dict, Any
from mgraph_ai.base.MGraph__Attribute   import MGraph__Attribute
from osbot_utils.helpers.Random_Guid    import Random_Guid
from osbot_utils.base_classes.Type_Safe import Type_Safe

class MGraph__Node(Type_Safe):
    attributes: Dict[Random_Guid, MGraph__Attribute]
    node_id   : Random_Guid