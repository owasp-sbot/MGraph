from typing                                                                     import Dict, Type
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                              import Schema__MGraph__Edge
from osbot_utils.helpers.Obj_Id                                                 import Obj_Id
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe


class Schema__MGraph__Time_Point__Created__Objects(Type_Safe):                              # The objects that were created

    time_point_id   : Obj_Id                                                # Node IDs created
    value_nodes     : Dict[Type[Schema__MGraph__Edge], Obj_Id]
    timezone_id     : Obj_Id
    utc_offset_id   : Obj_Id

    component_edges : Dict[Type[Schema__MGraph__Edge], Obj_Id]              # Edge IDs created
    timezone_edge   : Obj_Id
    offset_edge     : Obj_Id