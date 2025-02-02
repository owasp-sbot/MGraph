from typing                                              import Optional, Dict, Any
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data import Schema__MGraph__Node__Data

class Schema__Graph_RAG__Document__Data(Schema__MGraph__Node__Data):
    title        : str                                                             # Document title
    content      : str                                                             # Document content
    pub_date     : str                                                             # Publication date
    source_url   : Optional[str]            = None                                 # Source URL
    metadata     : Dict[str, Any]                                                 # Additional metadata
