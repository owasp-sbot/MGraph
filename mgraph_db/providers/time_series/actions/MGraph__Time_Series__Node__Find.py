from typing                                                                         import Optional, Set
from mgraph_db.mgraph.actions.MGraph__Data                                          import MGraph__Data
from mgraph_db.mgraph.actions.MGraph__Index                                         import MGraph__Index
from mgraph_db.mgraph.domain.Domain__MGraph__Node                                   import Domain__MGraph__Node
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Value__Int       import Schema__MGraph__Node__Value__Int
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Value__Timestamp import Schema__MGraph__Node__Value__Timestamp
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Time_Series__Edges     import Schema__MGraph__Time_Series__Edge__Timestamp
from osbot_utils.helpers.Obj_Id                                                     import Obj_Id
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe

class MGraph__Time_Series__Node__Find(Type_Safe):
    mgraph_data  : MGraph__Data                                                                      # Reference to MGraph data
    mgraph_index : MGraph__Index                                                                     # Reference to MGraph index

    def find_node_by_type_and_value(self, value: any, node_type: type) -> Optional[Obj_Id]:             # Generic method to find nodes by type and value
        node_type_name = node_type.__name__
        nodes_of_type  = self.mgraph_index.index_data.nodes_by_type.get(node_type_name, set())               # Use the type-specific index first to get nodes
        if not nodes_of_type:
            return None

        nodes_with_value = self.mgraph_index.index_data.nodes_by_field.get('value', {}).get(value, set())   # Then check the value index
        if not nodes_with_value:
            return None

        result_nodes = nodes_of_type & nodes_with_value                                                     # Find intersection
        if result_nodes:
            return next(iter(result_nodes))
        return None

    def find_timestamp_node(self, timestamp: int) -> Optional[Domain__MGraph__Node]:                # Find timestamp node
        node_id = self.find_node_by_type_and_value(timestamp, Schema__MGraph__Node__Value__Timestamp)
        if node_id:
            return self.mgraph_data.node(node_id)
        return None

    def find_time_point_by_timestamp(self, timestamp: int) -> Optional[Domain__MGraph__Node]:      # Find time point through timestamp
        # First find the timestamp node
        timestamp_node = self.find_timestamp_node(timestamp)
        if not timestamp_node:
            return None

        # Use edge type index to find connected time points
        edge_type = Schema__MGraph__Time_Series__Edge__Timestamp.__name__
        incoming_edges = self.mgraph_index.index_data.nodes_to_incoming_edges_by_type.get(timestamp_node.node_id, {}).get(edge_type, set())

        if incoming_edges:
            edge_id = next(iter(incoming_edges))
            from_node_id, _ = self.mgraph_index.index_data.edges_to_nodes[edge_id]
            return self.mgraph_data.node(from_node_id)

        return None

    def with_value(self, value: int) -> Optional[Domain__MGraph__Node]:                        # Find integer value node
        node_id = self.find_node_by_type_and_value(value,Schema__MGraph__Node__Value__Int)
        return node_id


    def get_node_value_by_edge_type(self, time_point_id: Obj_Id,
                                   edge_type_name: str) -> Optional[int]:                          # Get integer value connected to time point through specific edge type"""
        connected_node_id = self.mgraph_index.get_node_connected_to_node__outgoing(
            node_id=time_point_id,
            edge_type=edge_type_name
        )
        if connected_node_id:
            node = self.mgraph_data.node(connected_node_id)
            if node and node.node_data:
                return node.node_data.value
        return None