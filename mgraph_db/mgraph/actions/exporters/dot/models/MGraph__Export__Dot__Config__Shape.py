from osbot_utils.type_safe.Type_Safe import Type_Safe


class MGraph__Export__Dot__Config__Shape(Type_Safe):
    type       : str   = None    # Shape type (box, circle, etc)
    fill_color : str   = None    # Fill color
    rounded    : bool  = False   # Whether the shape is rounded
    style      : str   = None
    width      : float = None    # node width
    height     : float = None    # node height
    fixed_size : bool  = False   # whether size is fixed
