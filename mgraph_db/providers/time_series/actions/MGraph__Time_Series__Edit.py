from datetime                                                                    import datetime
from mgraph_db.mgraph.actions.MGraph__Edit                                       import MGraph__Edit
from mgraph_db.mgraph.domain.Domain__MGraph__Node                                import Domain__MGraph__Node
from mgraph_db.providers.time_series.actions.MGraph__Time_Point__Builder         import MGraph__Time_Point__Builder
from mgraph_db.providers.time_series.actions.MGraph__Time_Point__Create          import MGraph__Time_Point__Create
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Time_Point__Create__Data import \
    Schema__MGraph__Time_Point__Create__Data


class MGraph__Time_Series__Edit(MGraph__Edit):

    def create_time_point(self, **kwargs) -> Domain__MGraph__Node:
        time_point_builder = MGraph__Time_Point__Builder()
        create_data        = time_point_builder.from_components(**kwargs)
        time_point_node    = self.create_from__create_data(create_data)
        return time_point_node

    def create_from__datetime(self, dt: datetime) -> Domain__MGraph__Node:
        time_point_builder = MGraph__Time_Point__Builder()
        create_data        = time_point_builder.from_datetime(dt)
        time_point_node    = self.create_from__create_data(create_data)
        return time_point_node

    def create_from__create_data(self, create_data: Schema__MGraph__Time_Point__Create__Data):
        time_point_create  = MGraph__Time_Point__Create(mgraph_edit=self)
        created_objects    = time_point_create.execute(create_data)
        return self.data().node(created_objects.time_point__node_id)



