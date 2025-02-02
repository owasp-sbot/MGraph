from typing                                              import Any
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data import Schema__MGraph__Node__Data

class Schema__Simple__Node__Data(Schema__MGraph__Node__Data):
    value     : Any    = None
    name      : str    = None


