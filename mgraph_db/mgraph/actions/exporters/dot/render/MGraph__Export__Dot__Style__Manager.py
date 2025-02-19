from typing                                                                  import Set
from mgraph_db.mgraph.actions.exporters.dot.render.MGraph__Export__Dot__Base import MGraph__Export__Dot__Base

class MGraph__Export__Dot__Style__Manager(MGraph__Export__Dot__Base):

    def merge_styles(self, *style_sets: Set[str]) -> Set[str]:                   # Merge multiple style sets
        result = set()
        for styles in style_sets:
            result.update(styles)
        return result

    def get_node_type_styles(self, node_type: type) -> Set[str]:                 # Get styles for a node type
        styles = set()
        if node_type in self.config.type.shapes:
            shape_config = self.config.type.shapes[node_type]
            if shape_config.style:
                styles.update(shape_config.style.split(','))
        return styles

    def get_edge_type_styles(self, edge_type: type) -> Set[str]:                 # Get styles for an edge type
        styles = set()
        if edge_type in self.config.type.edge_style:
            styles.update(self.config.type.edge_style[edge_type].split(','))
        return styles