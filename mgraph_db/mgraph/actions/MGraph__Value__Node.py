from typing                                                             import Union, Type, Optional
from mgraph_db.mgraph.actions.MGraph__Edit                              import MGraph__Edit
from mgraph_db.mgraph.domain.Domain__MGraph__Node                       import Domain__MGraph__Node
from mgraph_db.mgraph.schemas.values.Schema__MGraph__Node__Value__Int   import Schema__MGraph__Node__Value__Int
from mgraph_db.mgraph.schemas.values.Schema__MGraph__Node__Value__Str   import Schema__MGraph__Node__Value__Str
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe


class MGraph__Value__Node(Type_Safe):
    mgraph_edit: MGraph__Edit

    def get_or_create(self, value: Union[int, str]) -> Optional[Domain__MGraph__Node]:                  # Get or create value node
        if   isinstance(value, int): return self.get_or_create__node_type(value, Schema__MGraph__Node__Value__Int)
        elif isinstance(value, str): return self.get_or_create__node_type(value, Schema__MGraph__Node__Value__Str)
        return None

    def get_or_create__node_type(self, value     : Union[int, str],                                     # Internal helper for typed nodes
                                       node_type : Type[Domain__MGraph__Node]
                                  ) -> Domain__MGraph__Node:
        with self.mgraph_edit.index() as _:
            matching_nodes = _.get_nodes_by_field('value', value)                                       # Find existing nodes
            type_nodes     = _.get_nodes_by_type (node_type    )
            result_nodes   = matching_nodes & type_nodes                                                # Get intersection

        if result_nodes:                                                                                # Return existing if found
            node_id = next(iter(result_nodes))
            return self.mgraph_edit.data().node(node_id)

        value_node = self.mgraph_edit.new_node(node_type = node_type,                                   # Create new if needed
                                               value     = value   )
        return value_node