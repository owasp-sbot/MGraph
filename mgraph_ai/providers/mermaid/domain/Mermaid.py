from mgraph_ai.mgraph.domain.MGraph                         import MGraph
from mgraph_ai.providers.mermaid.actions.Mermaid__Edit import Mermaid__Edit
from mgraph_ai.providers.mermaid.actions.Mermaid__Render    import Mermaid__Render
from mgraph_ai.providers.mermaid.domain.Mermaid__Graph      import Mermaid__Graph

class Mermaid(MGraph):
    graph: Mermaid__Graph

    def code(self) -> str:
        return self.render().code()

    def edit(self) -> Mermaid__Edit:
        return Mermaid__Edit(graph=self.graph)

    def render(self) -> Mermaid__Render:
        return Mermaid__Render(graph=self.graph)