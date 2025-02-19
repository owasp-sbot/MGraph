from typing                                                                                import Dict
from mgraph_db.mgraph.actions.exporters.dot.models.MGraph__Export__Dot__Config__Font       import MGraph__Export__Dot__Config__Font
from mgraph_db.mgraph.actions.exporters.dot.models.MGraph__Export__Dot__Config__Shape      import MGraph__Export__Dot__Config__Shape
from mgraph_db.mgraph.actions.exporters.dot.models.MGraph__Export__Dot__Config__Type__Node import MGraph__Export__Dot__Config__Type__Node
from osbot_utils.type_safe.Type_Safe                                                       import Type_Safe

class MGraph__Export__Dot__Config__Type(Type_Safe):
    edge_color    : Dict[type, str]                                         # Edge color colors by type
    edge_style    : Dict[type, str]                                         # Edge style colors by type
    edge_from     : Dict[type, MGraph__Export__Dot__Config__Type__Node]     # Styling for source nodes
    edge_to       : Dict[type, MGraph__Export__Dot__Config__Type__Node]     # Styling for target nodes
    shapes        : Dict[type, MGraph__Export__Dot__Config__Shape     ]     # Shape configurations by type
    fonts         : Dict[type, MGraph__Export__Dot__Config__Font      ]     # Font configurations by type
    value_shapes  : Dict[type, MGraph__Export__Dot__Config__Shape     ]     # shape config by value_type
    value_fonts   : Dict[type, MGraph__Export__Dot__Config__Font      ]     # font config by value_type


