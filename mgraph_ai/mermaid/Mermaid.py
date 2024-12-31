from osbot_utils.decorators.methods.cache_on_self import cache_on_self

from mgraph_ai.mermaid.Mermaid__Node import Mermaid__Node
from osbot_utils.base_classes.Type_Safe                    import Type_Safe
from mgraph_ai.mermaid.Mermaid__Data                       import Mermaid__Data
from mgraph_ai.mermaid.Mermaid__Renderer                   import Mermaid__Renderer
from mgraph_ai.mermaid.Mermaid__Edge                       import Mermaid__Edge
from mgraph_ai.mermaid.Mermaid__Graph                      import Mermaid__Graph
from mgraph_ai.mermaid.models.Mermaid__Diagram_Direction   import Diagram__Direction
from mgraph_ai.mermaid.models.Mermaid__Diagram__Type       import Diagram__Type

class Mermaid(Type_Safe):
    graph : Mermaid__Graph

    def add_directive(self, directive):
        self.renderer().config.directives.append(directive)
        return self

    def add_edge(self, from_node_key, to_node_key, label=None,attributes=None):
        nodes__by_key = self.data().nodes__by_key()
        from_node    = nodes__by_key.get(from_node_key)
        to_node      = nodes__by_key.get(to_node_key)
        if not from_node:
            from_node = self.add_node(key=from_node_key, label=from_node_key)
        if not to_node:
            to_node = self.add_node(key=to_node_key, label=to_node_key)

        kwargs       = dict(from_node_id = from_node.node_id,
                            to_node_id   = to_node  .node_id,
                            label        = label            ,
                            attributes   = attributes       )
        mermaid_edge = Mermaid__Edge(**kwargs)
        self.graph.edges.append(mermaid_edge)
        return mermaid_edge



    def add_node(self, **kwargs):
        return self.graph.add_node(Mermaid__Node(**kwargs))

    def data(self):
        return Mermaid__Data(graph=self.graph)

    def code(self):
        return self.renderer().code(self.nodes(), self.edges())

    def code_markdown(self):
        #self.code_create()
        self.code()
        rendered_lines = self.renderer().mermaid_code
        markdown = ['#### Mermaid Graph',
                    "```mermaid"        ,
                    *rendered_lines     ,
                    "```"               ]

        return '\n'.join(markdown)

    def edges(self):
        return self.graph.edges

    def print_code(self):
        print(self.code())

    def new_edge(self):
        from_node = self.new_node()
        to_node   = self.new_node()
        return self.add_edge(from_node.node_id, to_node.node_id)

    def new_node(self):
        return self.add_node()

    def nodes(self):
        return self.graph.nodes

    @cache_on_self
    def renderer(self):
        return Mermaid__Renderer(graph=self.graph)

    def set_direction(self, direction):
        if isinstance(direction, Diagram__Direction):
            self.renderer().diagram_direction = direction
        elif isinstance(direction, str) and direction in Diagram__Direction.__members__:
            self.renderer().diagram_direction = Diagram__Direction[direction]
        return self                             # If the value can't be set (not a valid name), do nothing

    def set_diagram_type(self, diagram_type):
        if isinstance(diagram_type, Diagram__Type):
            self.renderer().diagram_type = diagram_type

    def save(self, target_file=None):
        file_path = target_file or '/tmp/mermaid.md'

        with open(file_path, 'w') as file:
            file.write(self.code_markdown())
        return file_path