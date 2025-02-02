from typing                                              import Optional, Dict, Any
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge__Data import Schema__MGraph__Edge__Data

class Schema__Graph_RAG__Relation__Data(Schema__MGraph__Edge__Data):
    relation_type : str                                                             # Type of relationship
    confidence   : float                    = 1.0                                   # Confidence score
    context      : Optional[str]            = None                                  # Context where relation was found
    attributes   : Dict[str, Any]                                                   # Additional relation attributes
