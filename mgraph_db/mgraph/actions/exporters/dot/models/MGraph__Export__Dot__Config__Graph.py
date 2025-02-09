from osbot_utils.type_safe.Type_Safe import Type_Safe

class MGraph__Export__Dot__Config__Graph(Type_Safe):
    layout_engine : str   = None
    rank_dir      : str   = None                          # Direction of graph layout (TB, LR, etc)
    rank_sep      : float = None                          # Vertical separation between ranks
    node_sep      : float = None                          # Horizontal separation between nodes
    splines       : str   = None                          # Edge line style: 'line' (straight), 'polyline' (segments), 'ortho' (right angles), 'curved' (default)
    epsilon       : float = None                          # Edge routing control: lower values (0.1) = straighter lines, higher values = more curved