from osbot_utils.helpers.Random_Guid import Random_Guid
from osbot_utils.type_safe.Type_Safe import Type_Safe

class Schema__MGraph__Node_Config(Type_Safe):
    node_id   : Random_Guid
    node_type : type
    value_type: type