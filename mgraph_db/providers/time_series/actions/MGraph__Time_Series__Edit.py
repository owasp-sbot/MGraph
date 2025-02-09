from datetime                                                                               import datetime
from mgraph_db.mgraph.actions.MGraph__Edit                                                  import MGraph__Edit
from mgraph_db.mgraph.actions.MGraph__Index                                                 import MGraph__Index
from mgraph_db.mgraph.domain.Domain__MGraph__Node                                           import Domain__MGraph__Node
from mgraph_db.providers.time_series.actions.MGraph__Time_Series__Node__Create              import MGraph__Time_Series__Node__Create
from mgraph_db.providers.time_series.actions.MGraph__Time_Series__Node__Find                import MGraph__Time_Series__Node__Find
from osbot_utils.decorators.methods.cache_on_self                                           import cache_on_self


class MGraph__Time_Series__Edit(MGraph__Edit):

    def create_time_point(self, **kwargs) -> Domain__MGraph__Node:
        return self.node_create().create_time_point(**kwargs)

    def create_time_point__with_tz(self, timezone: str = 'UTC', **kwargs ) -> Domain__MGraph__Node:                                                               # Create time point with explicit timezone
        return self.node_create().create_time_point__with_tz(timezone=timezone, **kwargs)

    def create_time_point__from_datetime(self, dt: datetime) -> Domain__MGraph__Node:  # Create time point from datetime object
        return self.node_create().create_time_point__from_datetime(dt)

    @cache_on_self
    def index(self):
        return MGraph__Index.from_graph(self.graph)

    @cache_on_self
    def node_create(self):
        return MGraph__Time_Series__Node__Create(mgraph_edit=self, mgraph_index=self.index())

    @cache_on_self
    def node_find(self):
        return MGraph__Time_Series__Node__Find(mgraph_data=self.data(), mgraph_index=self.index())



