from typing                                                                             import Dict
from mgraph_db.mgraph.actions.exporters.dot.config.MGraph__Export__Dot__Config__Font    import MGraph__Export__Dot__Config__Font
from mgraph_db.mgraph.actions.exporters.dot.config.MGraph__Export__Dot__Config__Shape   import MGraph__Export__Dot__Config__Shape
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe

class MGraph__Export__Dot__Config__Type(Type_Safe):
    edge_color  : Dict[type, str]                                              # Edge color colors by type
    edge_style  : Dict[type, str]                                              # Edge style colors by type
    shapes      : Dict[type, MGraph__Export__Dot__Config__Shape]               # Shape configurations by type
    fonts       : Dict[type, MGraph__Export__Dot__Config__Font ]               # Font configurations by type