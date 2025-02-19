from mgraph_db.mgraph.actions.exporters.dot.models.MGraph__Export__Dot__Config__Font    import MGraph__Export__Dot__Config__Font
from mgraph_db.mgraph.actions.exporters.dot.models.MGraph__Export__Dot__Config__Shape   import MGraph__Export__Dot__Config__Shape
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe

class MGraph__Export__Dot__Config__Type__Node(Type_Safe):
    shapes   : MGraph__Export__Dot__Config__Shape                               # Shape configurations by type
    fonts    : MGraph__Export__Dot__Config__Font                                # Font configurations by type