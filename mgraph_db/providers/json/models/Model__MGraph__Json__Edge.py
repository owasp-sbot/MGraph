from mgraph_db.mgraph.models.Model__MGraph__Edge import Model__MGraph__Edge
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Edge import Schema__MGraph__Json__Edge


class Model__MGraph__Json__Edge(Model__MGraph__Edge):
    data: Schema__MGraph__Json__Edge

    def __init__(self, **kwargs):
        data      = kwargs.get('data') or self.__annotations__['data']()
        node_dict = dict(data=data)
        object.__setattr__(self, '__dict__', node_dict)