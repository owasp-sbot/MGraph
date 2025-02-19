from mgraph_db.mgraph.actions.exporters.dot.models.MGraph__Export__Dot__Config__Style import MGraph__Export__Dot__Config__Style

class MGraph__Export__Dot__Config__Edge(MGraph__Export__Dot__Config__Style):
    arrow_size : float = None                      # New: control arrow size
    arrow_head : str   = None                      # New: control arrow type
