from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data import Schema__MGraph__Node__Data


class Schema__MGraph__Json__Node__Property__Data(Schema__MGraph__Node__Data):       # For object property data
    name: str

    def __init__(self, **kwargs):
        name      = kwargs.get('name') or ''
        data_dict = dict(name = name)
        object.__setattr__(self, '__dict__', data_dict)