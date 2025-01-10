from osbot_utils.decorators.methods.cache_on_self                           import cache_on_self
from mgraph_ai.providers.mermaid.Mermaid__Render                            import Mermaid__Render
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node              import Schema__Mermaid__Node
from mgraph_ai.providers.mermaid.actions.Mermaid__Data                      import Mermaid__Data
from mgraph_ai.providers.mermaid.Mermaid__Edge                              import Mermaid__Edge
from mgraph_ai.providers.mermaid.domain.Mermaid__Graph                      import Mermaid__Graph
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Diagram_Direction import Schema__Mermaid__Diagram__Direction
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Diagram__Type     import Schema__Mermaid__Diagram__Type
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe


class Mermaid(Type_Safe):
    graph : Mermaid__Graph







    # def add_node(self, **kwargs):
    #     return self.graph.add_node(Schema__Mermaid__Node(**kwargs))

    # def data(self):
    #     return Mermaid__Data(graph=self.graph)

    # def code(self):
    #     return self.render().code()

    def code_markdown(self):
        #self.code_create()
        self.code()
        rendered_lines = self.render().mermaid_code
        markdown = ['#### Mermaid Graph',
                    "```mermaid"        ,
                    *rendered_lines     ,
                    "```"               ]

        return '\n'.join(markdown)

    def edges(self):
        return self.graph.edges()

    def print_code(self):
        print(self.code())

    def new_edge(self):
        from_node = self.new_node()
        to_node   = self.new_node()
        return self.add_edge(from_node.node_id, to_node.node_id)

    def new_node(self):
        return self.add_node()

    def nodes(self):
        return self.graph.nodes()

    @cache_on_self
    def render(self):
        return Mermaid__Render(graph=self.graph)

    def set_direction(self, direction):
        if isinstance(direction, Schema__Mermaid__Diagram__Direction):
            self.render().diagram_direction = direction
        elif isinstance(direction, str) and direction in Schema__Mermaid__Diagram__Direction.__members__:
            self.render().diagram_direction = Schema__Mermaid__Diagram__Direction[direction]
        return self                             # If the value can't be set (not a valid name), do nothing



    def save(self, target_file=None):
        file_path = target_file or '/tmp/mermaid.md'

        with open(file_path, 'w') as file:
            file.write(self.code_markdown())
        return file_path