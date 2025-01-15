from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node              import Schema__MGraph__Json__Node
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__Value__Data import Schema__MGraph__Json__Node__Value__Data


class Schema__MGraph__Json__Node__Value(Schema__MGraph__Json__Node):        # For JSON values (str, int, bool, null)
    node_data : Schema__MGraph__Json__Node__Value__Data
