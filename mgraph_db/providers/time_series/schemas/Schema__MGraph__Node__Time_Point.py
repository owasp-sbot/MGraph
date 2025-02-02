from mgraph_db.mgraph.schemas.Schema__MGraph__Node  import Schema__MGraph__Node
from mgraph_db.providers.time_series.schemas        import Schema__MGraph__Node__Time_Point__Data


class Schema__MGraph__Node__Time_Point(Schema__MGraph__Node):           # Time point node class
    node_data : Schema__MGraph__Node__Time_Point__Data