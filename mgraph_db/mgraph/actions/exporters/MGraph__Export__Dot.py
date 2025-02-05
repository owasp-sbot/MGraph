from typing                                                     import Dict, Any, List, Optional, Callable
from mgraph_db.mgraph.actions.exporters.MGraph__Export__Base    import MGraph__Export__Base
from mgraph_db.mgraph.domain.Domain__MGraph__Edge               import Domain__MGraph__Edge
from mgraph_db.mgraph.domain.Domain__MGraph__Node               import Domain__MGraph__Node
from osbot_utils.type_safe.Type_Safe                            import Type_Safe

SCHEMA_NAME__PREFIX__TO_REMOVE = 'Schema__MGraph__'

class MGraph__Export__Dot__Config(Type_Safe):

    font_name         : str   = ''                                                 # Font to use for nodes and edges
    font_color        : str   = ''
    font_size         : int   = None                                                      # Font size for edge labels
    node_color        : str   = ''
    node_shape        : str   = ''                                                          # Use to configure node shape
    node_style        : str   = ''
    rank_sep          : float = 0.8                         # todo: see if we actually use this                                        # Vertical separation between ranks
    show_edge_ids     : bool  = False                                                    # Whether to show edge IDs
    show_value        : bool  = False
    show_type         : bool  = False
    type_colors       : Dict[str, str]
    type_shape        : Dict[str, str]
    type_style        : Dict[str, str]

class MGraph__Export__Dot(MGraph__Export__Base):
    config     : MGraph__Export__Dot__Config
    on_add_node: Callable[[Domain__MGraph__Node, Dict[str, Any]], Dict[str, Any]]
    on_add_edge: Callable[[Domain__MGraph__Edge, Domain__MGraph__Node, Domain__MGraph__Node, Dict[str, Any]], None]

    def __init__(self, graph, config: Optional[MGraph__Export__Dot__Config] = None):
        super().__init__(graph=graph)
        self.config = config or MGraph__Export__Dot__Config()

    def create_node_attrs(self, node, include_type_label: bool = False) -> List[str]:                                   # Create list of node attributes for DOT format
        attrs = []
        label = "" #node.node_id
        if self.config.font_color : attrs.append(f'fontcolor="{self.config.font_color}"' )
        if self.config.font_size  : attrs.append(f'fontsize="{self.config.font_size}"' )
        if self.config.font_name  : attrs.append(f'fontname={self.config.font_name  }' )

        node_type = node.node.data.node_type.__name__

        if node_type in self.config.type_colors: attrs.append(f'fillcolor="{self.config.type_colors[node_type]}"')
        elif self.config.node_color            : attrs.append(f'fillcolor="{self.config.node_color}"'            )

        if node_type in self.config.type_shape : attrs.append(f'shape={self.config.type_shape[node_type]}' )
        elif self.config.node_shape            : attrs.append(f'shape={self.config.node_shape}'            )

        if node_type in self.config.type_style : attrs.append(f'style="{self.config.type_style[node_type]}"' )
        elif self.config.node_style            : attrs.append(f'style="{self.config.node_style}"'            )

        if self.config.show_value:
            if hasattr(node.node_data, 'value'):
                label = node.node_data.value
        elif self.config.show_type:
            label = self.fix_schema_name(node.node.data.node_type.__name__)

        # if include_type_label:
        #     node_type = self.fix_schema_name(node.node.data.node_type.__name__)
        #     attrs.extend([f'style="rounded,filled"' ,
        #                   f'fillcolor=lightblue'    ,
        #                   f'label="{node_type}"'   ])

        # if node.node_data:
        #     for field_name, field_value in node.node_data.__dict__.items():
        #         #attrs.append(f'{field_name}="{field_value}"')
        #         if self.config.show_value and (field_name in ['value', 'name']):
        #             attrs.append(f'label="{field_value}"')
        # elif self.config.show_value and not include_type_label:
        #     label = type(node.node.data).__name__.split('__').pop().lower()
        #     attrs.append(f'label="{label}"')
        if label:
            attrs.append(f'label="{label}"')
        return attrs

    def create_node_data(self, node) -> Dict[str, Any]:                             # Override to create DOT-specific node data
        node_view_data =  { 'id'   : str(node.node_id)           ,
                            'attrs': self.create_node_attrs(node) }
        if self.on_add_node:
            self.on_add_node(node, node_view_data)
        return node_view_data

    def create_edge_data(self, edge) -> Dict[str, Any]:                             # Override to create DOT-specific edge data
        edge_view_data =  { 'id'     : str(edge.edge_id)                ,
                            'source' : str(edge.from_node_id())         ,
                            'target' : str(edge.to_node_id())           ,
                            'type'   : edge.edge.data.edge_type.__name__,
                            'attrs'  : []                               }
        if self.on_add_edge:
            from_node = edge.from_node()
            to_node   = edge.to_node()
            if from_node and to_node:
                self.on_add_edge(edge, from_node, to_node, edge_view_data)
        return edge_view_data

    def format_node_line(self, node_id: str, attrs: List[str]) -> str:              # Format a single node line in DOT syntax
        attrs_str = f' [{", ".join(attrs)}]' if attrs else ''
        return f'  "{node_id}"{attrs_str}'

    def format_edge_line(self, source: str, target: str, edge_data: Dict[str, Any]) -> str:   # Updated to handle edge attributes
        attrs = []
        if self.config.show_edge_ids and 'label=':
            attrs.append(f'label="  {edge_data["id"]}"')
        if 'attrs' in edge_data and edge_data['attrs']:
            attrs.extend(edge_data['attrs'])

        attrs_str = f' [{", ".join(attrs)}]' if attrs else ''
        return f'  "{source}" -> "{target}"{attrs_str}'

    def format_output(self) -> str:                                                 # Override to format as DOT string
        lines = self.get_header()

        for node_data in self.context.nodes.values():                                                   # Add nodes
            lines.append(self.format_node_line(node_data["id"], node_data["attrs"]))

        for edge_data in self.context.edges.values():                                                   # Add edges
            lines.append(self.format_edge_line(edge_data["source"], edge_data["target"], edge_data))

        lines.append('}')
        return '\n'.join(lines)

    def to_types_view(self) -> str:                                                 # Export showing node structure
        lines = self.get_styled_header()
        self.config.show_edge_ids = False                                           # need to make sure this is False or we will also get an ID for the edge_id value
        self.config.node_shape    = 'box'

        with self.graph as _:                                                       # Output nodes with their types
            for node in _.nodes():
                node_attrs = self.create_node_attrs(node, include_type_label=True)
                lines.append(self.format_node_line(str(node.node_id), node_attrs))

            for edge in _.edges():                                                  # Output edges with type labels
                edge_type = self.fix_schema_name(edge.edge.data.edge_type.__name__)
                edge_data = { 'id'    : str(edge.edge_id)       ,
                              'source': str(edge.from_node_id()) ,
                              'target': str(edge.to_node_id())   ,
                              'type'  : edge_type                ,
                              'attrs' : [f'label="  {edge_type}"'] }
                lines.append(self.format_edge_line(edge_data["source"],
                                                 edge_data["target"],
                                                 edge_data))

        lines.append('}')
        return '\n'.join(lines)

    def collect_unique_elements(self):                                                      # Collect unique nodes and edges for schema view
        unique_nodes = {}
        unique_edges = set()

        with self.graph as _:
            for node in _.nodes():
                node_type = self.fix_schema_name(node.node.data.node_type.__name__)
                if node_type not in unique_nodes:
                    unique_nodes[node_type] = node

            for edge in _.edges():
                edge_type = self.fix_schema_name(edge.edge.data.edge_type            .__name__)
                from_type = self.fix_schema_name(edge.from_node().node.data.node_type.__name__)
                to_type = self.fix_schema_name(edge.to_node().node.data.node_type    .__name__)
                unique_edges.add((from_type, to_type, edge_type))

        return unique_nodes, unique_edges

    def to_schema_view(self) -> str:                                                # Export showing type relationships
        lines                      = self.get_styled_header()
        unique_nodes, unique_edges = self.collect_unique_elements()

        self.config.node_shape = 'box'

        for node_type, node in unique_nodes.items():                                # Add unique nodes
            node_attrs = self.create_node_attrs(node, include_type_label=True)
            lines.append(self.format_node_line(node_type, node_attrs))

        for from_type, to_type, edge_type in unique_edges:                          # Add unique edges
            edge_data = { 'id'    : edge_type    ,                                  # Use edge type as ID for schema view
                          'source': from_type     ,
                          'target': to_type       ,
                          'type'  : edge_type     ,
                          'attrs' : [] }
            lines.append(self.format_edge_line(from_type, to_type, edge_data))
        lines.append('}')
        return '\n'.join(lines)

    def get_header(self) -> List[str]:                                                      # Generate basic DOT header
        return ['digraph {']

    def get_styled_header(self) -> List[str]:                                               # Generate styled DOT header
        return [ 'digraph {',
                f'  graph [fontname="{self.config.font_name}", ranksep={self.config.rank_sep}]' ,
                f'  node  [fontname="{self.config.font_name}"]'                                 ,
                f'  edge  [fontname="{self.config.font_name}", fontsize={self.config.font_size}]']

    def fix_schema_name(self, value: str) -> str:                                           # Clean up schema names for display
        return value.replace(SCHEMA_NAME__PREFIX__TO_REMOVE, '').replace('_', ' ')



    def set_font__color           (self, color    : str): self.config.font_color     = color       ; return self
    def set_node__color           (self, color    : str): self.config.node_color     = color       ; return self
    def set_node__font            (self, name     : str): self.config.font_name      = name        ; return self
    def set_node__font__size      (self, size     : int): self.config.font_size      = size        ; return self
    def set_node__font__arial     (self,               ): self.config.font_name      = 'Arial'     ; return self
    def set_node__font__bold      (self,               ): self.config.font_name      = 'bold'      ; return self
    def set_node__shape           (self, shape    : str): self.config.node_shape     = shape       ; return self
    def set_node__shape__box      (self,               ): self.config.node_shape     = 'box'       ; return self
    def set_node__shape__circle   (self,               ): self.config.node_shape     = 'circle'    ; return self
    def set_node__shape__plaintext(self,               ): self.config.node_shape     = 'plaintext' ; return self
    def set_node__shape__point    (self,               ): self.config.node_shape     = 'point'     ; return self
    def set_node__shape__note     (self,               ): self.config.node_shape     = 'note'     ; return self
    def set_node__shape__square   (self,               ): self.config.node_shape     = 'square'     ; return self
    def set_node__shape__underline(self,               ): self.config.node_shape     = 'underline' ; return self
    def set_node__style__filled   (self                ): self.config.node_style    += 'filled,'   ; return self
    def set_node__style__rounded  (self                ): self.config.node_style    += 'rounded,'  ; return self
    def set_node__type_color      (self, node_type: str,
                                         color    : str): self.config.type_colors[node_type]= color; return self
    def set_node__type_shape      (self, node_type: str,
                                         shape    : str): self.config.type_shape [node_type]= shape; return self
    def set_node__type_style      (self, node_type: str,
                                         style    : str): self.config.type_style [node_type]= style; return self
    def show_edge__ids            (self                ): self.config.show_edge_ids  = True       ; return self
    def show_node__value          (self                ): self.config.show_value     = True         ; return self
    def show_node__type           (self                ): self.config.show_type      = True         ; return self

