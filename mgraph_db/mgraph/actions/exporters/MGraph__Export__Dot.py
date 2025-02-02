from typing                                                     import Dict, Any, List, Optional
from mgraph_db.mgraph.actions.exporters.MGraph__Export__Base    import MGraph__Export__Base
from osbot_utils.type_safe.Type_Safe                            import Type_Safe

class MGraph__Export__Dot__Config(Type_Safe):
    show_value    : bool = False                                                   # Whether to show value labels
    show_edge_ids : bool = True                                                    # Whether to show edge IDs
    font_name    : str  = "Arial"                                                  # Font to use for nodes and edges
    font_size    : int  = 10                                                       # Font size for edge labels
    rank_sep     : float = 0.8                                                     # Vertical separation between ranks

class MGraph__Export__Dot(MGraph__Export__Base):
    config: MGraph__Export__Dot__Config

    def create_node_data(self, node) -> Dict[str, Any]:                                # Override to create DOT-specific node data
        attrs = []
        if node.node_data:
            node_items = node.node_data.__dict__.items()
            if node_items:
                for field_name, field_value in node_items:
                    attrs.append(f'{field_name}="{field_value}"')
                    if self.config.show_value and (field_name in ['value', 'name']):
                        attrs.append(f'label="{field_value}"')
            elif self.config.show_value:
                label = type(node.node.data).__name__.split('__').pop().lower()
                attrs.append(f'label="{label}"')

        return {
            'id'   : str(node.node_id),
            'attrs': attrs
        }

    def create_edge_data(self, edge) -> Dict[str, Any]:                                # Override to create DOT-specific edge data
        return {
            'id'        : str(edge.edge_id)       ,
            'source'    : str(edge.from_node_id()),
            'target'    : str(edge.to_node_id())  ,
            'type'      : edge.edge.data.edge_type.__name__
        }

    def format_output(self) -> str:                                                     # Override to format as DOT string
        lines = self.get_header()

        # Add nodes
        for node_data in self.context.nodes.values():
            attrs_str = f' [{", ".join(node_data["attrs"])}]' if node_data["attrs"] else ''
            lines.append(f'  "{node_data["id"]}"{attrs_str}')

        # Add edges
        for edge_data in self.context.edges.values():
            edge_label = f"  {edge_data['id']}" if self.config.show_edge_ids else ""
            lines.append(f'  "{edge_data["source"]}" -> "{edge_data["target"]}" '
                        f'[label="{edge_label}"]')

        lines.append('}')
        return '\n'.join(lines)

    def to_types_view(self) -> str:                                                     # Export showing node structure
        lines = self.get_styled_header()

        with self.graph as _:
            # Output nodes with their types
            for node in _.nodes():
                node_id = node.node_id
                node_type = self.fix_schema_name(node.node.data.node_type.__name__)

                node_attrs = [
                    'shape=box'              ,
                    'style="rounded,filled"' ,
                    'fillcolor=lightblue'    ,
                    f'label="{node_type}"'
                ]

                if node.node_data:
                    for field_name, field_value in node.node_data.__dict__.items():
                        node_attrs.append(f'{field_name}="{field_value}"')

                attrs_str = f' [{", ".join(node_attrs)}]'
                lines.append(f'  "{node_id}"{attrs_str}')

            # Output edges with type labels
            for edge in _.edges():
                edge_type = self.fix_schema_name(edge.edge.data.edge_type.__name__)
                from_id = edge.from_node_id()
                to_id = edge.to_node_id()
                lines.append(f'  "{from_id}" -> "{to_id}" [label="  {edge_type}"]')

        lines.append('}')
        return '\n'.join(lines)

    def to_schema_view(self) -> str:                                                    # Export showing type relationships
        lines = self.get_styled_header()
        unique_nodes = set()
        unique_edges = set()

        with self.graph as _:
            # First pass: collect unique node types
            for node in _.nodes():
                node_type = self.fix_schema_name(node.node.data.node_type.__name__)
                if node_type not in unique_nodes:
                    unique_nodes.add(node_type)
                    node_attrs = [
                        'shape=box'             ,
                        'style="rounded,filled"',
                        'fillcolor=lightblue'
                    ]

                    if node.node_data:
                        for field_name, field_value in node.node_data.__dict__.items():
                            node_attrs.append(f'{field_name}="{field_value}"')

                    attrs_str = f' [{", ".join(node_attrs)}]'
                    lines.append(f'  "{node_type}"{attrs_str}')

            # Second pass: collect unique edge relationships
            for edge in _.edges():
                edge_type = self.fix_schema_name(edge.edge.data.edge_type.__name__)
                from_type = self.fix_schema_name(edge.from_node().node.data.node_type.__name__)
                to_type = self.fix_schema_name(edge.to_node().node.data.node_type.__name__)

                edge_key = (from_type, to_type, edge_type)
                if edge_key not in unique_edges:
                    unique_edges.add(edge_key)
                    lines.append(f'  "{from_type}" -> "{to_type}" [label="  {edge_type}"]')

        lines.append('}')
        return '\n'.join(lines)

    def get_header(self) -> List[str]:                                                 # Generate basic DOT header
        return ['digraph {']

    def get_styled_header(self) -> List[str]:                                         # Generate styled DOT header
        return [
            'digraph {',
            f'  graph [fontname="{self.config.font_name}", ranksep={self.config.rank_sep}]',
            f'  node  [fontname="{self.config.font_name}"]',
            f'  edge  [fontname="{self.config.font_name}", fontsize={self.config.font_size}]'
        ]

    @staticmethod
    def fix_schema_name(value: str) -> str:                                           # Clean up schema names for display
        return value.replace('Schema__MGraph__', '').replace('_', ' ')