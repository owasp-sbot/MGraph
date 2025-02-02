from typing                                              import Dict, Any, List
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data import Schema__MGraph__Node__Data

class Schema__Graph_RAG__Entity__Data(Schema__MGraph__Node__Data):
    name                 : str                                                       # Core entity name
    primary_domains      : List[str]                                                # Main domains this entity belongs to
    functional_roles     : List[str]                                                # Specific functions/purposes
    direct_relationships : List[Dict[str, Any]]                                     # Relationships with entities in text
    domain_relationships : List[Dict[str, Any]]                                     # Related domain knowledge concepts
    ecosystem            : Dict[str, Any]                                            # Technical/domain context
    confidence           : float              = 1.0





