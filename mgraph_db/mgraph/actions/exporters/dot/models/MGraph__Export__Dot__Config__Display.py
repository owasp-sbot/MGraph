from osbot_utils.type_safe.Type_Safe import Type_Safe

class MGraph__Export__Dot__Config__Display(Type_Safe):
    edge_ids            : bool  = False                      # Whether to show edge IDs
    edge_type           : bool  = False                      # Whether to show edge types (short version)
    edge_type_full_name : bool  = False                      # Whether to show edge types (using full type name)
    node_value          : bool  = False                      # Whether to show node values
    node_value_key      : bool  = False
    node_value_type     : bool  = False
    node_type           : bool = False                       # Whether to show node types (short version)
    node_type_full_name : bool = False                       # Whether to show node types (using full type name)