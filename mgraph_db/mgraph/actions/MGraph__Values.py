from typing                                                           import Union, Type, Tuple, Optional
from mgraph_db.mgraph.actions.MGraph__Edit                            import MGraph__Edit
from mgraph_db.mgraph.domain.Domain__MGraph__Node                     import Domain__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                    import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.values.Schema__MGraph__Node__Value__Int import Schema__MGraph__Node__Value__Int
from mgraph_db.mgraph.schemas.values.Schema__MGraph__Node__Value__Str import Schema__MGraph__Node__Value__Str
from osbot_utils.type_safe.Type_Safe                                  import Type_Safe


class MGraph__Values(Type_Safe):
    mgraph_edit: MGraph__Edit                                                                            # Reference to edit capabilities

    def get_or_create(self, value     : Union[int, str]           ,                                      # Value node creation (no edge)
                            node_type : Type[Domain__MGraph__Node]
                       ) -> Optional[Domain__MGraph__Node]:

        with self.mgraph_edit.index() as _:
            matching_nodes = _.get_nodes_by_field('value', value)                                        # Find nodes that have the same value
            type_nodes     = _.get_nodes_by_type (node_type)                                             # Find nodes that have the same type
            result_nodes   = matching_nodes & type_nodes                                                 # Get intersection of both

        if result_nodes:                                                                                 # Return existing if found
            return self.mgraph_edit.data().node(next(iter(result_nodes)))

        return self.mgraph_edit.new_node(node_type = node_type,                                          # Create new if needed
                                         value     = value   )

    def get_or_create_value(self, value     : Union[int, str]           ,                                # Value node with edge
                                 edge_type  : Type[Schema__MGraph__Edge] ,
                                 from_node  : Domain__MGraph__Node
                           ) -> Tuple[Domain__MGraph__Node, Domain__MGraph__Node]:                       # Returns (value_node, edge)

        node_type  = self.get_value_type(value)                                                         # Get correct node type
        value_node = self.get_or_create(value, node_type)                                               # Get or create the value node
        if value_node is None:                                                                          # Handle invalid value types
            raise ValueError(f"Unsupported value type: {type(value)}")

        edge = self.mgraph_edit.new_edge(edge_type    = edge_type          ,                           # Create edge to value
                                         from_node_id = from_node.node_id  ,
                                         to_node_id   = value_node.node_id )

        return value_node, edge

    def get_or_create_int_value(self, value     : int                        ,                          # Helper for integer values
                                     edge_type  : Type[Schema__MGraph__Edge] ,
                                     from_node  : Domain__MGraph__Node
                               ) -> Tuple[Domain__MGraph__Node, Domain__MGraph__Node]:
        return self.get_or_create_value(value, edge_type, from_node)

    def get_or_create_str_value(self, value     : str                        ,                          # Helper for string values
                                     edge_type  : Type[Schema__MGraph__Edge] ,
                                     from_node  : Domain__MGraph__Node
                               ) -> Tuple[Domain__MGraph__Node, Domain__MGraph__Node]:
        return self.get_or_create_value(value, edge_type, from_node)

    def get_linked_value(self, from_node : Domain__MGraph__Node       ,                                # Get value through edge type
                              edge_type : Type[Schema__MGraph__Edge]
                        ) -> Optional[Domain__MGraph__Node]:

        connected_node_id = self.mgraph_edit.index().get_node_connected_to_node__outgoing(
            node_id=from_node.node_id,
            edge_type=edge_type.__name__
        )
        if connected_node_id:
            return self.mgraph_edit.data().node(connected_node_id)
        return None

    def get_value_type(self, value: Union[int, str]) -> Optional[Type[Domain__MGraph__Node]]:          # Get node type for value
        if   isinstance(value, int): return Schema__MGraph__Node__Value__Int
        elif isinstance(value, str): return Schema__MGraph__Node__Value__Str
        return None