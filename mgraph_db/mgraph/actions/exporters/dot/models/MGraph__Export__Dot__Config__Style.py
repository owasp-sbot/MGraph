from mgraph_db.mgraph.actions.exporters.dot.models.MGraph__Export__Dot__Config__Font import MGraph__Export__Dot__Config__Font
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe

class MGraph__Export__Dot__Config__Style(Type_Safe):
    font     : MGraph__Export__Dot__Config__Font                # Font settings
    color    : str = None        