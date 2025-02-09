from typing                                                                  import List
from mgraph_db.mgraph.actions.exporters.dot.render.MGraph__Export__Dot__Base import MGraph__Export__Dot__Base
from mgraph_db.mgraph.domain.Domain__MGraph__Node                            import Domain__MGraph__Node


class MGraph__Export__Dot__Node__Renderer(MGraph__Export__Dot__Base):

    def create_node_attributes(self, node: Domain__MGraph__Node) -> List[str]:
        return (self.create_node_base_attributes   (node) +
                self.create_node_shape_attributes  (node) +
                self.create_node_font_attributes   (node) +
                self.create_node_style_attributes  (node) +
                self.create_node_label_attributes  (node))

    def create_node_base_attributes(self, node: Domain__MGraph__Node) -> List[str]:
        return []                                                                # Base implementation

    def create_node_shape_attributes(self, node: Domain__MGraph__Node) -> List[str]:
        attrs = []
        node_type = node.node.data.node_type


        if node_type in self.config.type.shapes:                                    # Apply type-specific shape configuration if it exists
            shape_config = self.config.type.shapes[node_type]
            if shape_config.type:       attrs.append(f'shape="{shape_config.type}"')
            if shape_config.fill_color: attrs.append(f'fillcolor="{shape_config.fill_color}"')
        return attrs

    def create_node_font_attributes(self, node: Domain__MGraph__Node) -> List[str]:
        attrs = []
        node_type = node.node.data.node_type

        if node_type in self.config.type.fonts:                                         # Apply type-specific font configuration if it exists
            font_config = self.config.type.fonts[node_type]
            if font_config.name:  attrs.append(f'fontname="{font_config.name}"')
            if font_config.size:  attrs.append(f'fontsize="{font_config.size}"')
            if font_config.color: attrs.append(f'fontcolor="{font_config.color}"')
        return attrs

    def create_node_style_attributes(self, node: Domain__MGraph__Node) -> List[str]:
        styles = set()
        node_type = node.node.data.node_type

        if node_type in self.config.type.shapes:
            shape_config = self.config.type.shapes[node_type]
            if shape_config.fill_color: styles.add('filled')
            if shape_config.rounded:    styles.add('rounded')
            if shape_config.style:      styles.update(shape_config.style.split(','))

        return [f'style="{",".join(sorted(styles))}"'] if styles else []

    def create_node_label_attributes(self, node: Domain__MGraph__Node) -> List[str]:
        if self.config.display.node_value and hasattr(node.node_data, 'value'):
            return [f'label="{node.node_data.value}"']
        elif self.config.display.node_type:
            node_type = node.node.data.node_type
            type_name = self.type_name__from__type(node_type)
            return [f'label="{type_name}"']
        return []

    def format_node_definition(self, node_id: str, attrs: List[str]) -> str:
        attrs_str = f' [{", ".join(attrs)}]' if attrs else ''
        return f'  "{node_id}"{attrs_str}'