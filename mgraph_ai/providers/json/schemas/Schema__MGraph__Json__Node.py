from osbot_utils.helpers.Obj_Id                          import Obj_Id
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node       import Schema__MGraph__Node

class Schema__MGraph__Json__Node(Schema__MGraph__Node):

    def __init__(self, **kwargs):
        #return super().__init__(**kwargs)
        node_data = kwargs.get('node_data') or self.__annotations__['node_data']()
        node_id   = kwargs.get('node_id'  ) or Obj_Id()
        node_type = kwargs.get('node_type') or self.__class__
        node_dict = dict(node_data = node_data,
                         node_id   = node_id  ,
                         node_type = node_type)
        object.__setattr__(self, '__dict__', node_dict)



