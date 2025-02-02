from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node import Schema__MGraph__Json__Node
from mgraph_db.mgraph.models.Model__MGraph__Node                 import Model__MGraph__Node

class Model__MGraph__Json__Node(Model__MGraph__Node):                                       # Base model class for JSON nodes
    data: Schema__MGraph__Json__Node

    def __init__(self, **kwargs):
        data      = kwargs.get('data') or self.__annotations__['data']()
        node_dict = dict(data=data)
        object.__setattr__(self, '__dict__', node_dict)