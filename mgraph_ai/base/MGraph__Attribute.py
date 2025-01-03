from typing                             import Dict, Any
from osbot_utils.helpers.Safe_Id        import Safe_Id
from osbot_utils.helpers.Random_Guid    import Random_Guid
from osbot_utils.base_classes.Type_Safe import Type_Safe

class MGraph__Attribute(Type_Safe):
    attr_id   : Random_Guid
    attr_name : Safe_Id
    attr_value: Any
    attr_type : type