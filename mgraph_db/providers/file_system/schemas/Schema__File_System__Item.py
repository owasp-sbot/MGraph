from mgraph_db.mgraph.schemas.Schema__MGraph__Node  import Schema__MGraph__Node
from osbot_utils.helpers.Timestamp_Now              import Timestamp_Now


class Schema__File_System__Item(Schema__MGraph__Node):
    created_at   : Timestamp_Now
    modified_at  : Timestamp_Now