from typing                                                 import Any
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node          import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data    import Schema__MGraph__Node__Data

class Schema__MGraph__Json__Node(Schema__MGraph__Node):                     # Base schema for JSON nodes
    pass

class Schema__MGraph__Json__Node__Value__Data(Schema__MGraph__Node__Data):  # Base schema for JSON node data
    value      : Any                                                        # The actual value
    value_type : type                                                       # Type of the value

class Schema__MGraph__Json__Node__Value(Schema__MGraph__Json__Node):        # For JSON values (str, int, bool, null)
    node_data : Schema__MGraph__Json__Node__Value__Data

class Schema__MGraph__Json__Node__Dict(Schema__MGraph__Json__Node):                 # For JSON objects {}
    pass

class Schema__MGraph__Json__Node__List(Schema__MGraph__Json__Node):                 # For JSON arrays []
    pass

class Schema__MGraph__Json__Node__Property__Data(Schema__MGraph__Node__Data):       # For object property data
    name: str

class Schema__MGraph__Json__Node__Property(Schema__MGraph__Json__Node):             # For object property names
    node_data : Schema__MGraph__Json__Node__Property__Data

