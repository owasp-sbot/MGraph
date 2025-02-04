from typing                                                                     import Optional
from mgraph_db.mgraph.actions.MGraph__Edit                                      import MGraph__Edit
from mgraph_db.mgraph.actions.MGraph__Index import MGraph__Index
from mgraph_db.mgraph.domain.Domain__MGraph__Node                               import Domain__MGraph__Node
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Time_Point   import Schema__MGraph__Node__Time_Point
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Value__Int   import Schema__MGraph__Node__Value__Int
from mgraph_db.providers.time_series.schemas.Schema__MGraph__TimeSeries__Edges  import Schema__MGraph__Time_Series__Edge__Year, Schema__MGraph__Time_Series__Edge__Month, Schema__MGraph__Time_Series__Edge__Day, Schema__MGraph__Time_Series__Edge__Hour, Schema__MGraph__Time_Series__Edge__Minute
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.helpers.Obj_Id                                                 import Obj_Id


class MGraph__Time_Series__Edit(MGraph__Edit):

    def create_time_point(self, year   : int            ,                                   # Create a complete time point
                                month  : Optional[int]  ,
                                day    : Optional[int]  ,
                                hour   : Optional[int]  ,
                                minute : Optional[int]  = None
                         )   -> Domain__MGraph__Node:
        time_point = self.new_node(node_type = Schema__MGraph__Node__Time_Point)            # Create a new time point with specified components


        year_value = self.get_or_create_int_value(year)                                    # Create year component
        self.new_edge(edge_type    = Schema__MGraph__Time_Series__Edge__Year,
                      from_node_id = time_point.node_id,
                      to_node_id   = year_value)


        if month is not None:                                                               # Add optional components
            month_value = self.get_or_create_int_value(month)
            self.new_edge(edge_type    = Schema__MGraph__Time_Series__Edge__Month,
                          from_node_id = time_point.node_id,
                          to_node_id   = month_value)

        if day is not None:
            day_value = self.get_or_create_int_value(day)
            self.new_edge(edge_type    = Schema__MGraph__Time_Series__Edge__Day,
                          from_node_id = time_point.node_id,
                          to_node_id   = day_value)

        if hour is not None:
            hour_value = self.get_or_create_int_value(hour)
            self.new_edge(edge_type    = Schema__MGraph__Time_Series__Edge__Hour,
                          from_node_id = time_point.node_id,
                          to_node_id   = hour_value)

        if minute is not None:
            minute_value = self.get_or_create_int_value(minute)
            self.new_edge(edge_type    = Schema__MGraph__Time_Series__Edge__Minute,
                          from_node_id = time_point.node_id,
                          to_node_id   = minute_value)

        return time_point

    def get_or_create_int_value(self, value: int) -> Obj_Id:           # Get existing or create new integer value node"""
        existing = self.find_int_value(value)
        if existing:
            return existing

        node = self.new_node(node_type = Schema__MGraph__Node__Value__Int,
                            value     = value)
        self.index().add_node(node.node.data)                          # Add new node to index
        return node.node_id

    @cache_on_self
    def index(self):
        return MGraph__Index.from_graph(self.graph)

    def find_int_value(self, value: int) -> Optional[Obj_Id]:                           # Find existing integer value node using index
        index          = self.index()                                                   # Get the graph index
        value_nodes    = index.get_nodes_by_type(Schema__MGraph__Node__Value__Int)      # First get all nodes of type Schema__MGraph__Node__Value__Int
        matching_nodes = index.get_nodes_by_field('value', value)                       # Then look for nodes with the specific value in their node_data
        result_nodes   = value_nodes & matching_nodes                                   # Find the intersection of value_type nodes and nodes with matching value

        if result_nodes:                                                                # Return the first matching node ID if any exist
            return next(iter(result_nodes))                                             # todo: review this usage and see if this is really the only way to think about this

        return None