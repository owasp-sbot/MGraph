from typing                                                                         import Dict, Any, List
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data                            import Schema__MGraph__Node__Data
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Direct_Relationship   import Schema__Graph_RAG__Direct_Relationship
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Domain_Relationship   import Schema__Graph_RAG__Domain_Relationship
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Ecosystem             import Schema__Graph_RAG__Ecosystem
from osbot_utils.helpers.Obj_Id                                                     import Obj_Id


class Schema__Graph_RAG__Entity__Data(Schema__MGraph__Node__Data):
    confidence           : float                                            # Confidence score (0-1)
    direct_relationships : List[Schema__Graph_RAG__Direct_Relationship]     # Relationships with entities in text
    domain_relationships : List[Schema__Graph_RAG__Domain_Relationship ]     # Related domain knowledge concepts
    ecosystem            : Schema__Graph_RAG__Ecosystem                     # Technical/domain context
    entity_id            : Obj_Id                                           # Unique entity identifier
    functional_roles     : List[str]                                        # Specific functions/purposes
    name                 : str                                              # Core entity name
    primary_domains      : List[str]                                        # Main domains this entity belongs to







