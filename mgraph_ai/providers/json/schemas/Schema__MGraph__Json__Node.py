from enum                                                   import Enum
from typing                                                 import Any
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node          import Schema__MGraph__Node

class Schema__MGraph__Json__Node__Type(Enum):
    VALUE    = 'value'
    DICT     = 'dict'
    LIST     = 'list'
    PROPERTY = 'property'

class Schema__MGraph__Json__Node(Schema__MGraph__Node):             # Base schema for JSON nodes
    pass

class Schema__MGraph__Json__Node__Value(Schema__MGraph__Json__Node):        # For JSON values (str, int, bool, null)
    value      : Any                                        # The actual value
    value_type : type                                       # Type of the value
    node_type  : Schema__MGraph__Json__Node__Type.VALUE             # VALUE type


class Schema__MGraph__Json__Node__Dict(Schema__MGraph__Json__Node):         # For JSON objects {}
    node_type  : Schema__MGraph__Json__Node__Type.DICT              # DICT type

class Schema__MGraph__Json__Node__List(Schema__MGraph__Json__Node):         # For JSON arrays []
    node_type  : Schema__MGraph__Json__Node__Type.LIST              # LIST type

class Schema__MGraph__Json__Node__Property(Schema__MGraph__Json__Node):     # For object property names
    name: str
    node_type  : Schema__MGraph__Json__Node__Type.PROPERTY          # PROPERTY type