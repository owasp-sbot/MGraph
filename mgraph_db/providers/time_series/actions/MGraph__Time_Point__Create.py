from typing                                                                               import Type, Tuple
from mgraph_db.mgraph.actions.MGraph__Edit                                                import MGraph__Edit
from mgraph_db.mgraph.domain.Domain__MGraph__Node                                         import Domain__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                                        import Schema__MGraph__Edge
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Time_Point__Create__Data     import Schema__MGraph__Time_Point__Create__Data
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Time_Point__Created__Objects import Schema__MGraph__Time_Point__Created__Objects
from osbot_utils.helpers.Obj_Id                                                           import Obj_Id
from osbot_utils.type_safe.Type_Safe                                                      import Type_Safe


class MGraph__Time_Point__Create(Type_Safe):
    mgraph_edit : MGraph__Edit

    def execute(self, create_data: Schema__MGraph__Time_Point__Create__Data) -> Schema__MGraph__Time_Point__Created__Objects:
        time_point = self.mgraph_edit.new_node(node_type=create_data.node_type__time_point)

        if create_data.datetime_str:                                             # Set the display value if available
            time_point.node_data.value = create_data.datetime_str

        value_nodes     = {}                                                     # Initialize tracking dictionaries
        component_edges = {}

        time_components = [(create_data.year  , create_data.edge_type__year  ),                # Define time components to process
                           (create_data.month , create_data.edge_type__month ),
                           (create_data.day   , create_data.edge_type__day   ),
                           (create_data.hour  , create_data.edge_type__hour  ),
                           (create_data.minute, create_data.edge_type__minute),
                           (create_data.second, create_data.edge_type__second)]

        for value, edge_type in time_components:                                 # Process each time component
            if value is not None:
                node_id, edge_id           = self.add_value_component(value      = value                       ,
                                                                      node_type  = create_data.node_type__value,
                                                                      edge_type  = edge_type                   ,
                                                                      from_node  = time_point                  )
                value_nodes    [edge_type] = node_id
                component_edges[edge_type] = edge_id

        tz_id, tz_edge = None, None
        if create_data.timezone:                                                 # Handle timezone if present
            tz_id, tz_edge = self.add_timezone_component(timezone     = create_data.timezone  ,
                                                         utc_offset   = create_data.utc_offset ,
                                                         create_data  = create_data            ,
                                                         time_point   = time_point             )


        return Schema__MGraph__Time_Point__Created__Objects(time_point_id   = time_point.node_id ,
                                                            value_nodes     = value_nodes        ,
                                                            component_edges = component_edges     ,
                                                            timezone_id     = tz_id              ,
                                                            timezone_edge   = tz_edge            ,
                                                            utc_offset_id   = None               ,                               # todo: add support for this
                                                            offset_edge     = None               )

    def add_timezone_component(self, timezone    : str                                      ,
                                     utc_offset  : int                                      ,
                                     create_data : Schema__MGraph__Time_Point__Create__Data ,
                                     time_point  : Domain__MGraph__Node
                                ) -> Tuple[Obj_Id, Obj_Id]:                                     # Returns (timezone_node_id, timezone_edge_id)
        tz_node = self.mgraph_edit.new_node(node_type = create_data.node_type__timezone,            # Create timezone node
                                            value     = timezone)

        tz_edge = self.mgraph_edit.new_edge(edge_type    = create_data.edge_type__tz,               # Create edge to timezone
                                            from_node_id = time_point.node_id      ,
                                            to_node_id   = tz_node.node_id)

        if utc_offset is not None:                                                                  # Add UTC offset if available
            offset_node  = self.mgraph_edit.new_node(node_type = create_data.node_type__utc_offset,
                                                     value     = utc_offset)
            offset_edge = self.mgraph_edit.new_edge (edge_type    = create_data.edge_type__offset,                 # Link timezone to offset
                                                     from_node_id = tz_node.node_id            ,
                                                     to_node_id   = offset_node.node_id)

            # todo: we need to also capture the offset_edge

        return tz_node.node_id, tz_edge.edge_id     # todo: this should be a dict with data (not a tuple)

    def add_value_component(self, value    : int                        ,
                                  node_type : Type[Domain__MGraph__Node] ,
                                  edge_type : Type[Schema__MGraph__Edge] ,
                                  from_node : Domain__MGraph__Node
                             ) -> Tuple[Obj_Id, Obj_Id]:                                        # Returns (value_node_id, edge_id)
        value_node = self.get_or_create_value_node(value, node_type)                            # Get or create value node

        edge = self.mgraph_edit.new_edge(edge_type    = edge_type          ,                    # Create edge to value node
                                         from_node_id = from_node.node_id  ,
                                         to_node_id   = value_node.node_id )

        return value_node.node_id, edge.edge_id

    def get_or_create_value_node(self, value: int, node_type: Type[Domain__MGraph__Node]) -> Domain__MGraph__Node:  # todo: refactor this to the core of MGraph (edit, create or index)
        matching_nodes = self.mgraph_edit.index().get_nodes_by_field('value', value)        # Check if value node exists
        type_nodes     = self.mgraph_edit.index().get_nodes_by_type(node_type)
        result_nodes   = matching_nodes & type_nodes                                        # Find intersection

        if result_nodes:                                                                    # Return existing node if found
            return self.mgraph_edit.data().node(next(iter(result_nodes)))

        value_node = self.mgraph_edit.new_node(node_type = node_type,                       # Create new value node if needed
                                               value     = value)

        return value_node