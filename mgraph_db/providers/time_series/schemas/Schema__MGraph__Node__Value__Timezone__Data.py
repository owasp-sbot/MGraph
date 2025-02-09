from typing                                              import Optional
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data import Schema__MGraph__Node__Data

class Schema__MGraph__Node__Value__Timezone__Data(Schema__MGraph__Node__Data):
    zone_name : Optional[str]  = None                                                    # IANA timezone name (e.g., 'America/New_York')
    utc_offset: Optional[int]  = None                                                    # Offset in minutes from UTC
