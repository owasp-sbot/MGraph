from mgraph_db.mgraph.schemas.Schema__MGraph__Node                                         import Schema__MGraph__Node
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Node__Value__UTC_Offset__Data import Schema__MGraph__Node__Value__UTC_Offset__Data


class Schema__MGraph__Node__Value__UTC_Offset(Schema__MGraph__Node):
    node_data: Schema__MGraph__Node__Value__UTC_Offset__Data
