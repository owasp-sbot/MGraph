from datetime                                                                               import datetime
from typing                                                                                 import Optional, Type
from zoneinfo                                                                               import ZoneInfo
from mgraph_db.mgraph.actions.MGraph__Edit                                                  import MGraph__Edit
from mgraph_db.mgraph.actions.MGraph__Index                                                 import MGraph__Index
from mgraph_db.mgraph.domain.Domain__MGraph__Node                                           import Domain__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                                          import Schema__MGraph__Edge
from mgraph_db.providers.time_series.actions.MGraph__Time_Series__Node__Find                import MGraph__Time_Series__Node__Find
from mgraph_db.providers.time_series.actions.MGraph__Time_Series__Node__Find_Or_Create      import MGraph__Time_Series__Node__Find_Or_Create
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Time_Point               import Schema__MGraph__Node__Time_Point
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Value__Timezone__Name    import Schema__MGraph__Node__Value__Timezone__Name
from mgraph_db.providers.time_series.schemas.Schema__MGraph__TimeSeries__Edges              import Schema__MGraph__Time_Series__Edge__Year, Schema__MGraph__Time_Series__Edge__Month, Schema__MGraph__Time_Series__Edge__Day, Schema__MGraph__Time_Series__Edge__Hour, Schema__MGraph__Time_Series__Edge__Minute, Schema__MGraph__Time_Series__Edge__Second, Schema__MGraph__Time_Series__Edge__UTC_Offset, Schema__MGraph__Time_Series__Edge__Timezone
from osbot_utils.decorators.methods.cache_on_self                                           import cache_on_self
from osbot_utils.helpers.Obj_Id                                                             import Obj_Id
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe


class MGraph__Time_Series__Node__Create(Type_Safe):
    mgraph_edit : MGraph__Edit
    mgraph_index: MGraph__Index

    def add_time_component(self, time_point_id: Obj_Id,
                                 value        : int,
                                 edge_type    : Type[Schema__MGraph__Edge]
                            ) -> None:
        value_node_id = self.node_find_or_create().get_or_create__int_value(value)
        self.mgraph_edit.new_edge(edge_type    = edge_type,
                                  from_node_id = time_point_id,
                                  to_node_id   = value_node_id)

    def create_time_point(self, year   : Optional[int] = None,
                                month  : Optional[int] = None,
                                day    : Optional[int] = None,
                                hour   : Optional[int] = None,
                                minute : Optional[int] = None,
                                second : Optional[int] = None
                           ) -> Domain__MGraph__Node:

        time_point = self.mgraph_edit.new_node(node_type=Schema__MGraph__Node__Time_Point)

        components = [(year  , Schema__MGraph__Time_Series__Edge__Year     ),
                      (month , Schema__MGraph__Time_Series__Edge__Month    ),
                      (day   , Schema__MGraph__Time_Series__Edge__Day      ),
                      (hour  , Schema__MGraph__Time_Series__Edge__Hour     ),
                      (minute, Schema__MGraph__Time_Series__Edge__Minute   ),
                      (second, Schema__MGraph__Time_Series__Edge__Second   )]

        for value, edge_type in components:
            if value is not None:
                self.add_time_component(time_point.node_id, value, edge_type)

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

    def create_time_point__with_tz(self, year: int = None, month : int = None, day   : int = None,
                                         hour: int = None, minute: int = None, second: int = None, timezone: str = 'UTC'
                                    ) -> Domain__MGraph__Node:                                                               # Create time point with explicit timezone

        time_point      = self.create_time_point   (year      = year, month=month, day=day,hour=hour, minute=minute, second=second)
        tz_name_node    = self.mgraph_edit.new_node(node_type = Schema__MGraph__Node__Value__Timezone__Name, value = timezone)  # Create timezone name node
        tz              = ZoneInfo(timezone)                                                                                 # Calculate UTC offset
        dt              = datetime(year, month, day, hour, minute, tzinfo=tz)
        utc_offset      = int(dt.utcoffset().total_seconds() / 60)
        utc_offset_node = self.node_find_or_create().get_or_create__utc_offset(utc_offset)                                                         # Create or reuse UTC offset node

        formatted_time             = self.format_datetime_string(year, month, day, hour, minute, timezone)
        time_point.node_data.value = formatted_time

        self.mgraph_edit.new_edge(edge_type    = Schema__MGraph__Time_Series__Edge__UTC_Offset,                                          # Connect timezone name to UTC offset
                      from_node_id = tz_name_node.node_id,
                      to_node_id   = utc_offset_node.node_id)


        self.mgraph_edit.new_edge(edge_type    = Schema__MGraph__Time_Series__Edge__Timezone,                       # Connect time point to timezone name
                      from_node_id = time_point.node_id,
                      to_node_id   = tz_name_node.node_id)

        return time_point

    def format_datetime_string(self, year: int, month: int, day: int,                     # Format datetime string
                                     hour: int, minute: int, tz: str) -> str:
        dt = datetime(year, month, day, hour, minute, tzinfo=ZoneInfo(tz))
        return dt.strftime("%a, %d %b %Y %H:%M:%S %z")

    @cache_on_self
    def node_find(self):
        return MGraph__Time_Series__Node__Find          (mgraph_data=self.mgraph_edit.data(), mgraph_index=self.mgraph_index)

    @cache_on_self
    def node_find_or_create(self):
        return MGraph__Time_Series__Node__Find_Or_Create(mgraph_edit=self.mgraph_edit, mgraph_index=self.mgraph_index)