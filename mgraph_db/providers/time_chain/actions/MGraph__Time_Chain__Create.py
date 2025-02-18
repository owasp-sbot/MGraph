from datetime                                                                   import datetime, UTC
from typing                                                                     import Optional
from mgraph_db.mgraph.actions.MGraph__Edit                                      import MGraph__Edit
from mgraph_db.mgraph.actions.MGraph__Values                                    import MGraph__Values
from mgraph_db.mgraph.domain.Domain__MGraph__Node                               import Domain__MGraph__Node
from mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Edge    import Schema__MGraph__Time_Chain__Edge__Month, Schema__MGraph__Time_Chain__Edge__Day, Schema__MGraph__Time_Chain__Edge__Hour, Schema__MGraph__Time_Chain__Edge__Minute, Schema__MGraph__Time_Chain__Edge__Second, Schema__MGraph__Time_Chain__Edge__Source, Schema__MGraph__Time_Chain__Edge__Year
from mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Types import (Year, Year_Month,
                                                                                      Year_Month_Day,
                                                                                      Year_Month_Day_Hour,
                                                                                      Year_Month_Day_Hour_Minute,
                                                                                      Year_Month_Day_Hour_Minute_Second,
                                                                                      Year_Month_Day_Hour_Minute_Second_Source)
from osbot_utils.decorators.methods.cache_on_self                             import cache_on_self
from osbot_utils.helpers.Obj_Id import Obj_Id
from osbot_utils.type_safe.Type_Safe                                          import Type_Safe


class MGraph__Time_Chain__Create(Type_Safe):
    mgraph_edit: MGraph__Edit

    @cache_on_self
    def values(self) -> MGraph__Values:                                                               # Value node factory accessor
        return MGraph__Values(mgraph_edit=self.mgraph_edit)

    def create_from_datetime(self, dt       : datetime,
                                   source_id: Optional[Obj_Id] = None
                              ) -> Domain__MGraph__Node:                                      # Create chain from datetime

        if dt.tzinfo is None:                                                                        # Ensure datetime has timezone
            dt = dt.replace(tzinfo=UTC)

        key_year   = f'{dt.year   }'
        key_month  = f'{key_year  }:{dt.month   }'
        key_day    = f'{key_month }:{dt.day     }'
        key_hour   = f'{key_day   }:{dt.hour    }'
        key_minute = f'{key_hour  }:{dt.minute }'
        key_second = f'{key_minute}:{dt.second }'

        year_node   = self.values().get_or_create(value=Year                             (dt.year  ), key = key_year  ) # Create nodes for each level
        month_node  = self.values().get_or_create(value=Year_Month                       (dt.month ), key = key_month )
        day_node    = self.values().get_or_create(value=Year_Month_Day                   (dt.day   ), key = key_day   )
        hour_node   = self.values().get_or_create(value=Year_Month_Day_Hour              (dt.hour  ), key = key_hour  )
        minute_node = self.values().get_or_create(value=Year_Month_Day_Hour_Minute       (dt.minute), key = key_minute)
        second_node = self.values().get_or_create(value=Year_Month_Day_Hour_Minute_Second(dt.second), key = key_second)

        self.mgraph_edit.get_or_create_edge(edge_type    = Schema__MGraph__Time_Chain__Edge__Month,
                                            from_node_id = year_node.node_id,
                                            to_node_id   = month_node.node_id)

        self.mgraph_edit.get_or_create_edge(edge_type    = Schema__MGraph__Time_Chain__Edge__Day,
                                            from_node_id = month_node.node_id,
                                            to_node_id   = day_node.node_id)

        self.mgraph_edit.get_or_create_edge(edge_type    = Schema__MGraph__Time_Chain__Edge__Hour,
                                            from_node_id = day_node.node_id,
                                            to_node_id   = hour_node.node_id)

        self.mgraph_edit.get_or_create_edge(edge_type    = Schema__MGraph__Time_Chain__Edge__Minute,
                                            from_node_id = hour_node.node_id,
                                            to_node_id   = minute_node.node_id)

        self.mgraph_edit.get_or_create_edge(edge_type    = Schema__MGraph__Time_Chain__Edge__Second,
                                            from_node_id = minute_node.node_id,
                                            to_node_id   = second_node.node_id)
        if source_id:                                                                               # Connect to source if provided
            source_node = self.create_source_node(source_id)
            self.mgraph_edit.get_or_create_edge(edge_type    = Schema__MGraph__Time_Chain__Edge__Source,
                                                from_node_id = second_node.node_id,
                                                to_node_id   = source_node.node_id)


        return year_node                                                                             # Return the root of the chain

    def create_partial_chain(self, year     : Optional[int] = None,                                 # Create chain with partial precision
                                   month    : Optional[int] = None,
                                   day      : Optional[int] = None,
                                   hour     : Optional[int] = None,
                                   minute   : Optional[int] = None,
                                   second   : Optional[int] = None) -> Optional[Domain__MGraph__Node]:

        prev_node = None
        components = [(year  , f'{year}'                                        , Year                             , Schema__MGraph__Time_Chain__Edge__Year  ),                                   # Define component sequence
                      (month , f'{year}:{month}'                                , Year_Month                       , Schema__MGraph__Time_Chain__Edge__Month ),
                      (day   , f'{year}:{month}:{day}:'                         , Year_Month_Day                   , Schema__MGraph__Time_Chain__Edge__Day   ),
                      (hour  , f'{year}:{month}:{day}:{hour}'                   , Year_Month_Day_Hour              , Schema__MGraph__Time_Chain__Edge__Hour  ),
                      (minute, f'{year}:{month}:{day}:{hour}:{minute}'          , Year_Month_Day_Hour_Minute       , Schema__MGraph__Time_Chain__Edge__Minute),
                      (second, f'{year}:{month}:{day}:{hour}:{minute}:{second}' , Year_Month_Day_Hour_Minute_Second ,Schema__MGraph__Time_Chain__Edge__Second)]

        for raw_value, key, value_type, edge_type in components:                                                        # Create and link each component
            if raw_value is None:
                break
            value        = value_type(raw_value)
            current_node = self.values().get_or_create(value=value_type(value), key=key)

            if prev_node:
                self.mgraph_edit.new_edge(edge_type    = edge_type           ,
                                          from_node_id = prev_node   .node_id,
                                          to_node_id   = current_node.node_id)

            prev_node = current_node

        return prev_node                                                                           # Return the last node in the chain

    def create_source_node(self, source_id: Obj_Id) -> Domain__MGraph__Node:                        # Create source node
        return self.values().get_or_create(value=Year_Month_Day_Hour_Minute_Second_Source(str(source_id)))
