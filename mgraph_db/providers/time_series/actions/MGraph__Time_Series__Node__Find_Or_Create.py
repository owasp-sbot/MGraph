from mgraph_db.mgraph.actions.MGraph__Edit                                              import MGraph__Edit
from mgraph_db.mgraph.actions.MGraph__Index                                             import MGraph__Index
from mgraph_db.mgraph.domain.Domain__MGraph__Node                                       import Domain__MGraph__Node
from mgraph_db.providers.time_series.actions.MGraph__Time_Series__Node__Find            import MGraph__Time_Series__Node__Find
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Value__Int           import Schema__MGraph__Node__Value__Int
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Value__UTC_Offset    import Schema__MGraph__Node__Value__UTC_Offset
from osbot_utils.decorators.methods.cache_on_self                                       import cache_on_self
from osbot_utils.helpers.Obj_Id                                                         import Obj_Id
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe


class MGraph__Time_Series__Node__Find_Or_Create(Type_Safe):
    mgraph_edit : MGraph__Edit
    mgraph_index: MGraph__Index

    def get_or_create__int_value(self, value: int) -> Obj_Id:           # Get existing or create new integer value node"""
        existing = self.node_find().with_value(value)
        if existing:
            return existing

        node = self.mgraph_edit.new_node(node_type = Schema__MGraph__Node__Value__Int,
                                         value     = value)
        self.mgraph_index.add_node(node.node.data)                          # Add new node to index
        return node.node_id

    def get_or_create__utc_offset(self, offset: int) -> Domain__MGraph__Node:                            # Helper to get or create UTC offset node
        matching_nodes = self.mgraph_index.get_nodes_by_field('value', offset)                           # First try to find existing UTC offset node
        utc_nodes      = self.mgraph_index.get_nodes_by_type(Schema__MGraph__Node__Value__UTC_Offset)
        result_nodes   = matching_nodes & utc_nodes                                                      # Find intersection of value match and type match

        if result_nodes:                                                                                 # Return existing node if found
            return self.mgraph_edit.data().node(next(iter(result_nodes)))

        offset_node = self.mgraph_edit.new_node(node_type = Schema__MGraph__Node__Value__UTC_Offset,     # Create new UTC offset node if none exists
                                                value     = offset)

        self.mgraph_index.add_node(offset_node.node.data)                                                # Add to index for future reuse
        return offset_node

    @cache_on_self
    def node_find(self):
        return MGraph__Time_Series__Node__Find(mgraph_data=self.mgraph_edit.data(), mgraph_index=self.mgraph_index)