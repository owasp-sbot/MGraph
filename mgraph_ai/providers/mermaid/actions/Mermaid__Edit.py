from typing                                                                 import Dict

from mgraph_ai.providers.mermaid.domain.Mermaid__Node import Mermaid__Node
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Render__Config    import Schema__Mermaid__Render__Config
from osbot_utils.utils.Misc                                                 import random_text
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute                     import Schema__MGraph__Attribute
from mgraph_ai.providers.mermaid.domain.Mermaid__Edge                       import Mermaid__Edge
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Diagram_Direction import Schema__Mermaid__Diagram__Direction
from osbot_utils.helpers.Safe_Id                                            import Safe_Id
from mgraph_ai.providers.mermaid.actions.Mermaid__Data                      import Mermaid__Data
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Diagram__Type     import Schema__Mermaid__Diagram__Type
from osbot_utils.decorators.methods.cache_on_self                           import cache_on_self
from mgraph_ai.mgraph.actions.MGraph__Edit                                  import MGraph__Edit
from mgraph_ai.providers.mermaid.domain.Mermaid__Graph                      import Mermaid__Graph


class Mermaid__Edit(MGraph__Edit):
    graph      : Mermaid__Graph

    def add_directive(self, directive):
        self.render_config().directives.append(directive)
        return self

    def add_edge(self, from_node_key:Safe_Id, to_node_key:Safe_Id, label:str=None, attributes:Dict=None) -> Mermaid__Edge:
        nodes__by_key = self.data().nodes__by_key()
        from_node     = nodes__by_key.get(from_node_key)            # todo: add method to data to get these nodes
        to_node       = nodes__by_key.get(to_node_key  )            # todo: add config option to auto create node on edges (where that node doesn't exist)
        if from_node is None:
            from_node = self.new_node(key=from_node_key)
        if to_node  is None:
            to_node = self.new_node(key=to_node_key)

        from_node_id    = from_node.node_id()
        to_node_id      = to_node.node_id()
        edge_attributes = {}
        if attributes:
            for key,value in attributes.items():                            # todo: refactor this logic of creating attributes into a separate method (since this will also be needed for the nodes)
                attribute = Schema__MGraph__Attribute(attribute_name=key, attribute_value=value, attribute_type=type(value))
                edge_attributes[attribute.attribute_id] = attribute

        edge = self.graph.new_edge(from_node_id=from_node_id, to_node_id=to_node_id, attributes=edge_attributes)
        if label:
            edge.edge.data.label = label                                    # todo: find a better way to set these properties (this
        return edge

    def add_node(self, **kwargs) -> Mermaid__Node:                          # todo: see if we need this method
        return self.new_node(**kwargs)

    @cache_on_self
    def data(self):
        return Mermaid__Data(graph=self.graph)                  # todo: look at the best way to do this (i.e. give access to this class the info inside data)

    def new_edge(self):
        from_node_key = random_text('node', lowercase=True)
        to_node_key   = random_text('node', lowercase=True)
        return self.add_edge(from_node_key, to_node_key)

    def render_config(self) -> Schema__Mermaid__Render__Config:         # todo: review this since we really should be able to access the Mermaid__Render__Config outside the Mermaid__Render object
        return self.graph.model.data.render_config

    def set_diagram_type(self, diagram_type):                           # todo: should this be moved into the render class?
        if isinstance(diagram_type, Schema__Mermaid__Diagram__Type):
            self.render_config().diagram_type = diagram_type

    def set_direction(self, direction):
        if isinstance(direction, Schema__Mermaid__Diagram__Direction):
            self.render_config().diagram_direction = direction
        elif isinstance(direction, str) and direction in Schema__Mermaid__Diagram__Direction.__members__:
            self.render_config().diagram_direction = Schema__Mermaid__Diagram__Direction[direction]
        return self                             # If the value can't be set (not a valid name), do nothing

    def new_node(self, **kwargs) -> Mermaid__Node:
        return super().new_node(**kwargs)