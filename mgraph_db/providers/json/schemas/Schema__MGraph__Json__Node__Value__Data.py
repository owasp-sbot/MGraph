from typing                                              import Any
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data import Schema__MGraph__Node__Data

class Schema__MGraph__Json__Node__Value__Data(Schema__MGraph__Node__Data):  # Base schema for JSON node data
    value      : Any                                                        # The actual value
    value_type : type                                                       # Type of the value

    def __init__(self, **kwargs):
        data_dict = dict(value      = kwargs.get('value'     ),             # note: no type checking here
                         value_type = kwargs.get('value_type'))             # note: no type checking here
        object.__setattr__(self, '__dict__', data_dict)