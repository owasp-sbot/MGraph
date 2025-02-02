from typing                                                                  import Type
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Document__Data import Schema__Graph_RAG__Document__Data
from osbot_utils.helpers.Obj_Id                                              import Obj_Id
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                           import Schema__MGraph__Node

class Schema__Graph_RAG__Document(Schema__MGraph__Node):
    node_data : Schema__Graph_RAG__Document__Data                                  # Document node data
    node_id   : Obj_Id                                                            # Unique node identifier
    node_type : Type['Schema__Graph_RAG__Document']