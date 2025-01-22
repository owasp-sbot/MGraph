from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge                       import Schema__MGraph__Edge
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Edge__Config import Schema__MGraph__Json__Edge__Config
from osbot_utils.helpers.Obj_Id                                          import Obj_Id


class Schema__MGraph__Json__Edge(Schema__MGraph__Edge):
    #edge_config : Schema__MGraph__Json__Edge__Config           # todo: figure out how to add this without breaking the self.__annotations__ below

    def __init__(self, **kwargs):
        edge_config  = kwargs.get('edge_config' ) or self.__annotations__['edge_config']()
        edge_data    = kwargs.get('edge_data'   ) or self.__annotations__['edge_data'  ]()
        edge_type    = kwargs.get('edge_type'   ) or self.__class__
        from_node_id = kwargs.get('from_node_id') or Obj_Id()
        to_node_id   = kwargs.get('to_node_id'  ) or Obj_Id()

        edge_dict = dict(edge_config  = edge_config ,
                         edge_data    = edge_data   ,
                         edge_type    = edge_type   ,
                         from_node_id = from_node_id,
                         to_node_id   = to_node_id  )
        object.__setattr__(self, '__dict__', edge_dict)