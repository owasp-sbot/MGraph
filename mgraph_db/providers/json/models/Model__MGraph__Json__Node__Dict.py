from mgraph_db.providers.json.models.Model__MGraph__Json__Node          import Model__MGraph__Json__Node
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Dict  import Schema__MGraph__Json__Node__Dict


class Model__MGraph__Json__Node__Dict(Model__MGraph__Json__Node):                          # Model class for JSON object nodes
    data: Schema__MGraph__Json__Node__Dict

    def __init__(self, **kwargs):
        data      = kwargs.get('data') or self.__annotations__['data']()
        node_dict = dict(data=data)
        object.__setattr__(self, '__dict__', node_dict)