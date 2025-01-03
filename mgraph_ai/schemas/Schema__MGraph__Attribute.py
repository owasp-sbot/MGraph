from typing                             import Any
from osbot_utils.helpers.Safe_Id        import Safe_Id
from osbot_utils.helpers.Random_Guid    import Random_Guid
from osbot_utils.type_safe.Type_Safe    import Type_Safe

class Schema__MGraph__Attribute(Type_Safe):
    attribute_id   : Random_Guid
    attribute_name : Safe_Id
    attribute_value: Any
    attribute_type : type