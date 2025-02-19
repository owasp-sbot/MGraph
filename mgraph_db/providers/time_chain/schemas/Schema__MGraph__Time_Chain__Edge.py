from mgraph_db.mgraph.schemas.Schema__MGraph__Edge import Schema__MGraph__Edge

class Schema__MGraph__Time_Chain__Edge__Year   (Schema__MGraph__Edge): pass    # Edge connecting Year to Year_Month nodes
class Schema__MGraph__Time_Chain__Edge__Month  (Schema__MGraph__Edge): pass    # Edge connecting Year_Month to Year_Month_Day nodes
class Schema__MGraph__Time_Chain__Edge__Day    (Schema__MGraph__Edge): pass    # Edge connecting Year_Month_Day to Year_Month_Day_Hour nodes
class Schema__MGraph__Time_Chain__Edge__Hour   (Schema__MGraph__Edge): pass    # Edge connecting Year_Month_Day_Hour to Year_Month_Day_Hour_Minute nodes
class Schema__MGraph__Time_Chain__Edge__Minute (Schema__MGraph__Edge): pass    # Edge connecting Year_Month_Day_Hour_Minute to Year_Month_Day_Hour_Minute_Second nodes
class Schema__MGraph__Time_Chain__Edge__Second (Schema__MGraph__Edge): pass    # Edge from Year_Month_Day_Hour_Minute_Second to other components
class Schema__MGraph__Time_Chain__Edge__Source (Schema__MGraph__Edge): pass    # Edge connecting Second node to source node
