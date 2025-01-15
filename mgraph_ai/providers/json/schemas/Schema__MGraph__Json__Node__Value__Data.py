from typing                                              import Any
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data import Schema__MGraph__Node__Data

class Schema__MGraph__Json__Node__Value__Data(Schema__MGraph__Node__Data):  # Base schema for JSON node data
    value      : Any                                                        # The actual value
    value_type : type                                                       # Type of the value