from mgraph_db.providers.json.models.Model__MGraph__Json__Node          import Model__MGraph__Json__Node
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__List  import Schema__MGraph__Json__Node__List


class Model__MGraph__Json__Node__List(Model__MGraph__Json__Node):                          # Model class for JSON array nodes
    data: Schema__MGraph__Json__Node__List

    def __init__(self, **kwargs):
        data      = kwargs.get('data') or self.__annotations__['data']()
        node_dict = dict(data=data)
        object.__setattr__(self, '__dict__', node_dict)