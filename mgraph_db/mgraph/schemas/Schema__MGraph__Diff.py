from typing                          import Set
from osbot_utils.helpers.Obj_Id      import Obj_Id
from osbot_utils.type_safe.Type_Safe import Type_Safe


class Schema__MGraph__Diff(Type_Safe):
    nodes_added         : Set[Obj_Id]
    nodes_removed       : Set[Obj_Id]
    nodes_modified      : Set[Obj_Id]
    edges_added         : Set[Obj_Id]
    edges_removed       : Set[Obj_Id]
    edges_modified      : Set[Obj_Id]
    nodes_count_diff    : int
    edges_count_diff    : int