from mgraph_db.mgraph.actions.exporters.dot.models.MGraph__Export__Dot__Config__Display    import MGraph__Export__Dot__Config__Display
from mgraph_db.mgraph.actions.exporters.dot.models.MGraph__Export__Dot__Config__Edge       import MGraph__Export__Dot__Config__Edge
from mgraph_db.mgraph.actions.exporters.dot.models.MGraph__Export__Dot__Config__Graph      import MGraph__Export__Dot__Config__Graph
from mgraph_db.mgraph.actions.exporters.dot.models.MGraph__Export__Dot__Config__Node       import MGraph__Export__Dot__Config__Node
from mgraph_db.mgraph.actions.exporters.dot.models.MGraph__Export__Dot__Config__Type       import MGraph__Export__Dot__Config__Type
from osbot_utils.type_safe.Type_Safe                                                       import Type_Safe

class MGraph__Export__Dot__Config(Type_Safe):
    graph       : MGraph__Export__Dot__Config__Graph                        # Graph-level settings
    node        : MGraph__Export__Dot__Config__Node                         # Global node settings
    edge        : MGraph__Export__Dot__Config__Edge                         # Global edge settings
    display     : MGraph__Export__Dot__Config__Display                      # Display flags
    type        : MGraph__Export__Dot__Config__Type                         # Type-specific overrides