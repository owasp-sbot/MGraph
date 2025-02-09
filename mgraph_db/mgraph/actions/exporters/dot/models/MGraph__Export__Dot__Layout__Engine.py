from enum import Enum


class MGraph__Export__Dot__Layout__Engine(str, Enum):
    DOT       : str = 'dot'                     # Directed graphs, hierarchical layouts
    NEATO     : str = 'neato'                   # Undirected graphs, spring model layout
    TWOPI     : str = 'twopi'                   # Radial layout
    CIRCO     : str = 'circo'                   # Circular layout
    FDP       : str = 'fdp'                     # Undirected graphs, force-directed
    SFDP      : str = 'sfdp'                    # Large graphs, multiscale force-directed
    PATCHWORK : str = 'patchwork'               # Array-based layout, squarified treemaps
    OSAGE     : str = 'osage'                   # Array-based layout