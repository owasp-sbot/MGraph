from datetime import datetime
from typing                                                                     import Optional
from zoneinfo import ZoneInfo

from mgraph_db.mgraph.actions.MGraph__Edit                                      import MGraph__Edit
from mgraph_db.mgraph.actions.MGraph__Index                                     import MGraph__Index
from mgraph_db.mgraph.domain.Domain__MGraph__Node                               import Domain__MGraph__Node
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Time_Point   import Schema__MGraph__Node__Time_Point
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Value__Int   import Schema__MGraph__Node__Value__Int
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Value__Timezone__Name import \
    Schema__MGraph__Node__Value__Timezone__Name
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Value__UTC_Offset import \
    Schema__MGraph__Node__Value__UTC_Offset
from mgraph_db.providers.time_series.schemas.Schema__MGraph__TimeSeries__Edges import \
    Schema__MGraph__Time_Series__Edge__Year, Schema__MGraph__Time_Series__Edge__Month, \
    Schema__MGraph__Time_Series__Edge__Day, Schema__MGraph__Time_Series__Edge__Hour, \
    Schema__MGraph__Time_Series__Edge__Minute, Schema__MGraph__Time_Series__Edge__UTC_Offset, \
    Schema__MGraph__Time_Series__Edge__Timezone, Schema__MGraph__Time_Series__Edge__Second
from osbot_utils.decorators.methods.cache_on_self                               import cache_on_self
from osbot_utils.helpers.Obj_Id                                                 import Obj_Id


class MGraph__Time_Series__Edit(MGraph__Edit):

    def create_time_point(self, year    : Optional[int] = None,                                   # Create a complete time point
                                month   : Optional[int] = None,
                                day     : Optional[int] = None,
                                hour    : Optional[int] = None,
                                minute  : Optional[int] = None,
                                second  : Optional[int] = None
                         )   -> Domain__MGraph__Node:
        time_point = self.new_node(node_type = Schema__MGraph__Node__Time_Point)            # Create a new time point with specified components


        year_value = self.get_or_create__int_value(year)                                    # Create year component
        self.new_edge(edge_type    = Schema__MGraph__Time_Series__Edge__Year,
                      from_node_id = time_point.node_id,
                      to_node_id   = year_value)


        if month is not None:                                                               # Add optional components
            month_value = self.get_or_create__int_value(month)
            self.new_edge(edge_type    = Schema__MGraph__Time_Series__Edge__Month,
                          from_node_id = time_point.node_id,
                          to_node_id   = month_value)

        if day is not None:
            day_value = self.get_or_create__int_value(day)
            self.new_edge(edge_type    = Schema__MGraph__Time_Series__Edge__Day,
                          from_node_id = time_point.node_id,
                          to_node_id   = day_value)

        if hour is not None:
            hour_value = self.get_or_create__int_value(hour)
            self.new_edge(edge_type    = Schema__MGraph__Time_Series__Edge__Hour,
                          from_node_id = time_point.node_id,
                          to_node_id   = hour_value)

        if minute is not None:
            minute_value = self.get_or_create__int_value(minute)
            self.new_edge(edge_type    = Schema__MGraph__Time_Series__Edge__Minute,
                          from_node_id = time_point.node_id,
                          to_node_id   = minute_value)

        if second is not None:
            second_value = self.get_or_create__int_value(second)
            self.new_edge(edge_type    = Schema__MGraph__Time_Series__Edge__Second,
                          from_node_id = time_point.node_id,
                          to_node_id   = second_value)

        return time_point

    def create_time_point__with_tz(self, year: int = None, month : int = None, day   : int = None,
                                         hour: int = None, minute: int = None, second: int = None, timezone: str = 'UTC'
                                    ) -> Domain__MGraph__Node:                                                               # Create time point with explicit timezone

        time_point      = self.create_time_point(year      = year, month=month, day=day,hour=hour, minute=minute, second=second)
        tz_name_node    = self.new_node         (node_type = Schema__MGraph__Node__Value__Timezone__Name, value = timezone)  # Create timezone name node
        tz              = ZoneInfo(timezone)                                                                                 # Calculate UTC offset
        dt              = datetime(year, month, day, hour, minute, tzinfo=tz)
        utc_offset      = int(dt.utcoffset().total_seconds() / 60)
        utc_offset_node = self.get_or_create__utc_offset(utc_offset)                                                         # Create or reuse UTC offset node

        formatted_time             = self.format_datetime_string(year, month, day, hour, minute, timezone)
        time_point.node_data.value = formatted_time

        self.new_edge(edge_type    = Schema__MGraph__Time_Series__Edge__UTC_Offset,                                          # Connect timezone name to UTC offset
                      from_node_id = tz_name_node.node_id,
                      to_node_id   = utc_offset_node.node_id)


        self.new_edge(edge_type    = Schema__MGraph__Time_Series__Edge__Timezone,                       # Connect time point to timezone name
                      from_node_id = time_point.node_id,
                      to_node_id   = tz_name_node.node_id)

        return time_point

    def create_time_point__from_datetime(self, dt: datetime) -> Domain__MGraph__Node:  # Create time point from datetime object
        timezone = dt.tzinfo.tzname(None) if dt.tzinfo else 'UTC'
        time_point = self.create_time_point__with_tz(year     = dt.year  ,
                                                     month    = dt.month ,
                                                     day      = dt.day   ,
                                                     hour     = dt.hour  ,
                                                     minute   = dt.minute,
                                                     second   = dt.second,
                                                     timezone = timezone )
        return time_point

    def get_or_create__int_value(self, value: int) -> Obj_Id:           # Get existing or create new integer value node"""
        existing = self.find_int_value(value)
        if existing:
            return existing

        node = self.new_node(node_type = Schema__MGraph__Node__Value__Int,
                            value     = value)
        self.index().add_node(node.node.data)                          # Add new node to index
        return node.node_id

    def get_or_create__utc_offset(self, offset: int) -> Domain__MGraph__Node:              # Helper to get or create UTC offset node
        matching_nodes = self.index().get_nodes_by_field('value', offset)                   # First try to find existing UTC offset node
        utc_nodes = self.index().get_nodes_by_type(Schema__MGraph__Node__Value__UTC_Offset)
        result_nodes = matching_nodes & utc_nodes                                           # Find intersection of value match and type match

        if result_nodes:                                                                    # Return existing node if found
            return self.data().node(next(iter(result_nodes)))

        offset_node = self.new_node(node_type = Schema__MGraph__Node__Value__UTC_Offset,    # Create new UTC offset node if none exists
                                    value     = offset)

        self.index().add_node(offset_node.node.data)                                       # Add to index for future reuse
        return offset_node

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

    def format_datetime_string(self, year: int, month: int, day: int,                     # Format datetime string
                                     hour: int, minute: int, tz: str) -> str:
        dt = datetime(year, month, day, hour, minute, tzinfo=ZoneInfo(tz))
        return dt.strftime("%a, %d %b %Y %H:%M:%S %z")