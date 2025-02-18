from typing                          import Type
from osbot_utils.type_safe.Type_Safe import Type_Safe

class Schema__MGraph__Node__Value__Data(Type_Safe):
    value      : str                                # Raw value stored as string
    key        : str
    value_type : Type = str                         # Python type of the value (default to being a str)