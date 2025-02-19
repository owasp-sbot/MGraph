from typing                          import Dict, Any
from osbot_utils.helpers.Obj_Id      import Obj_Id
from osbot_utils.type_safe.Type_Safe import Type_Safe

class Schema__MGraph__Index__Data(Type_Safe):
    edges_to_nodes                 : Dict[Obj_Id, tuple[Obj_Id,  Obj_Id ]]  # edge_id -> (from_node_id, to_node_id)
    edges_by_type                  : Dict[str   , set  [Obj_Id          ]]  # edge_type -> set of edge_ids
    edges_types                    : Dict[Obj_Id, str                    ]
    nodes_by_type                  : Dict[str   , set  [Obj_Id          ]]  # node_type -> set of node_ids
    nodes_types                    : Dict[Obj_Id, str]
    nodes_to_incoming_edges        : Dict[Obj_Id, set  [Obj_Id          ]]  # node_id -> set of incoming edge_ids
    nodes_to_incoming_edges_by_type: Dict[Obj_Id, Dict [str, set[Obj_Id]]]
    nodes_to_outgoing_edges        : Dict[Obj_Id, set  [Obj_Id          ]]  # node_id -> set of outgoing edge_ids
    nodes_to_outgoing_edges_by_type: Dict[Obj_Id, Dict [str, set[Obj_Id]]]

