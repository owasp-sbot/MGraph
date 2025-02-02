from mgraph_db.mgraph.schemas.Schema__MGraph__Edge__Config import Schema__MGraph__Edge__Config
from osbot_utils.helpers.Obj_Id                            import Obj_Id

class Schema__MGraph__Json__Edge__Config(Schema__MGraph__Edge__Config):

    def __init__(self, **kwargs):
        edge_id   = kwargs.get('edge_id') or Obj_Id()
        data_dict = dict(edge_id=edge_id)
        object.__setattr__(self, '__dict__', data_dict)