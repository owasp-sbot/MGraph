from typing                                                                  import Type
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Relation__Data import Schema__Graph_RAG__Relation__Data
from osbot_utils.helpers.Obj_Id                                              import Obj_Id
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                           import Schema__MGraph__Edge

class Schema__Graph_RAG__Relation(Schema__MGraph__Edge):
    edge_data    : Schema__Graph_RAG__Relation__Data                               # Relation edge data
    edge_type    : Type['Schema__Graph_RAG__Relation']                            # Edge type information
    from_node_id : Obj_Id                                                         # Source entity ID
    to_node_id   : Obj_Id                                                         # Target entity ID
