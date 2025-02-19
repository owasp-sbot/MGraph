from enum                                                                        import Enum
from typing                                                                      import Dict, Optional
from mgraph_db.mgraph.actions.exporters.dot.MGraph__Export__Dot                  import MGraph__Export__Dot
from mgraph_db.providers.time_series.schemas.Schema__MGraph__Time_Series__Edges  import Schema__MGraph__Time_Series__Edge__Year, Schema__MGraph__Time_Series__Edge__Month, Schema__MGraph__Time_Series__Edge__Day, Schema__MGraph__Time_Series__Edge__Hour, Schema__MGraph__Time_Series__Edge__Minute, Schema__MGraph__Time_Series__Edge__Second
from osbot_utils.type_safe.Type_Safe                                             import Type_Safe

class MGraph__Export__Dot__Time_Series__Colors__Scheme(str, Enum):
    DEFAULT: str = 'default'
    OCEAN  : str = 'ocean'
    FOREST : str = 'forest'
    SUNSET : str = 'sunset'

class MGraph__Export__Dot__Time_Series__Colors(Type_Safe):      # Helper class for managing Time Series color schemes in DOT exports
    dot_export : MGraph__Export__Dot

    def apply_color_scheme(self, scheme_name    : str           = 'default',
                                 year_color     : Optional[str] = None     ,
                                 month_color    : Optional[str] = None     ,
                                 day_color      : Optional[str] = None     ,
                                 hour_color     : Optional[str] = None     ,
                                 minute_color   : Optional[str] = None     ,
                                 second_color   : Optional[str] = None     ) -> MGraph__Export__Dot:        # Apply a color scheme to the time series nodes

        colors = self.get_scheme_colors(scheme_name)
        
        
        if year_color  : colors['year']   = year_color                                                      # Override any specified colors
        if month_color : colors['month']  = month_color
        if day_color   : colors['day']    = day_color
        if hour_color  : colors['hour']   = hour_color
        if minute_color: colors['minute'] = minute_color
        if second_color: colors['second'] = second_color
        
        return self.apply_colors(colors)

    def get_scheme_colors(self, scheme_name: str) -> Dict[str, str]:   # Get the colors for a named scheme
        schemes = {
            'default': {
                'year'  : '#4363D8',    # Strong Blue
                'month' : '#6F5EBF',    # Blue-Purple
                'day'   : '#9759A3',    # Purple
                'hour'  : '#C15587',    # Purple-Pink
                'minute': '#E34D6B',    # Pink-Red
                'second': '#FF4646'     # Bright Red
            },
            'ocean': {
                'year'  : '#023E8A',    # Deep Ocean
                'month' : '#0077B6',    # Ocean Blue
                'day'   : '#0096C7',    # Sea Blue
                'hour'  : '#00B4D8',    # Light Sea
                'minute': '#48CAE4',    # Sky Blue
                'second': '#90E0EF'     # Pale Blue
            },
            'forest': {
                'year'  : '#1B4332',    # Dark Forest
                'month' : '#2D6A4F',    # Forest Green
                'day'   : '#40916C',    # Sage
                'hour'  : '#52B788',    # Mint
                'minute': '#74C69D',    # Light Mint
                'second': '#95D5B2'     # Pale Green
            },
            'sunset': {
                'year'  : '#7D2181',    # Deep Purple
                'month' : '#B5179E',    # Bright Purple
                'day'   : '#E01E84',    # Pink
                'hour'  : '#F15C5C',    # Coral
                'minute': '#F7996E',    # Peach
                'second': '#FAC858'     # Gold
            }
        }
        return schemes.get(scheme_name, schemes['default'])

    def apply_colors(self, colors: Dict[str, str]) -> MGraph__Export__Dot:                 # Apply the color scheme to the DOT export
        return (self.dot_export
            .set_edge_to_node__type_fill_color(Schema__MGraph__Time_Series__Edge__Year  , colors['year']  )
            .set_edge_to_node__type_fill_color(Schema__MGraph__Time_Series__Edge__Month , colors['month'] )
            .set_edge_to_node__type_fill_color(Schema__MGraph__Time_Series__Edge__Day   , colors['day']   )
            .set_edge_to_node__type_fill_color(Schema__MGraph__Time_Series__Edge__Hour  , colors['hour']  )
            .set_edge_to_node__type_fill_color(Schema__MGraph__Time_Series__Edge__Minute, colors['minute'])
            .set_edge_to_node__type_fill_color(Schema__MGraph__Time_Series__Edge__Second, colors['second']))