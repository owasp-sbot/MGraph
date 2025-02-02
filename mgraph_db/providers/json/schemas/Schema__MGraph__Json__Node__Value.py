from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node              import Schema__MGraph__Json__Node
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value__Data import Schema__MGraph__Json__Node__Value__Data


class Schema__MGraph__Json__Node__Value(Schema__MGraph__Json__Node):        # For JSON values (str, int, bool, null)
    node_data : Schema__MGraph__Json__Node__Value__Data

    def __init__(self, **kwargs):
        node_data = kwargs.get('node_data')
        if isinstance(node_data, dict):
            node_data = Schema__MGraph__Json__Node__Value__Data(**node_data)
        kwargs['node_data'] = node_data
        super().__init__(**kwargs)