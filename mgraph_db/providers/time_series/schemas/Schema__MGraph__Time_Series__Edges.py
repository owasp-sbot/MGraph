from mgraph_db.mgraph.schemas.Schema__MGraph__Edge import Schema__MGraph__Edge
from osbot_utils.type_safe.Type_Safe               import Type_Safe

# class Schema__MGraph__Time_Series__Edge__Data(Type_Safe):                                                    # Base edge data
#     edge_type : str                                                                                         # Type of temporal relationship

class Schema__MGraph__Time_Series__Edge__Year       (Schema__MGraph__Edge): pass
class Schema__MGraph__Time_Series__Edge__Month      (Schema__MGraph__Edge): pass
class Schema__MGraph__Time_Series__Edge__Day        (Schema__MGraph__Edge): pass
class Schema__MGraph__Time_Series__Edge__Hour       (Schema__MGraph__Edge): pass
class Schema__MGraph__Time_Series__Edge__Minute     (Schema__MGraph__Edge): pass
class Schema__MGraph__Time_Series__Edge__Second     (Schema__MGraph__Edge): pass
class Schema__MGraph__Time_Series__Edge__Millisecond(Schema__MGraph__Edge): pass
class Schema__MGraph__Time_Series__Edge__Microsecond(Schema__MGraph__Edge): pass
class Schema__MGraph__Time_Series__Edge__Nanosecond (Schema__MGraph__Edge): pass

class Schema__MGraph__Time_Series__Edge__Source_Id  (Schema__MGraph__Edge): pass
class Schema__MGraph__Time_Series__Edge__Timezone   (Schema__MGraph__Edge): pass
class Schema__MGraph__Time_Series__Edge__Timestamp  (Schema__MGraph__Edge): pass     # Edge to timestamp value node
class Schema__MGraph__Time_Series__Edge__UTC_Offset (Schema__MGraph__Edge): pass

