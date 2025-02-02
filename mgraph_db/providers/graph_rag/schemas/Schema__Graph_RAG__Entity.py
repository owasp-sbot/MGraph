from typing                                                                import Type
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Entity__Data import Schema__Graph_RAG__Entity__Data
from osbot_utils.helpers.Obj_Id                                            import Obj_Id
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                         import Schema__MGraph__Node

class Schema__Graph_RAG__Entity(Schema__MGraph__Node):
    node_data : Schema__Graph_RAG__Entity__Data                                     # Entity node data
    node_id   : Obj_Id                                                             # Unique node identifier
    node_type : Type['Schema__Graph_RAG__Entity']                                  # Node type information
