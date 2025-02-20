from typing                                                 import Type
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge__Data    import Schema__MGraph__Edge__Data
from osbot_utils.helpers.Obj_Id                             import Obj_Id
from osbot_utils.type_safe.Type_Safe                        import Type_Safe

class Schema__MGraph__Edge(Type_Safe):
    edge_id       : Obj_Id
    edge_data     : Schema__MGraph__Edge__Data
    edge_type     : Type['Schema__MGraph__Edge']
    from_node_id  : Obj_Id
    to_node_id    : Obj_Id