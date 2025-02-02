from mgraph_ai.mgraph.MGraph                                    import MGraph
from mgraph_ai.providers.mermaid.actions.Mermaid__Edit          import Mermaid__Edit
from mgraph_ai.providers.mermaid.actions.Mermaid__Render        import Mermaid__Render
from mgraph_ai.providers.mermaid.domain.Domain__Mermaid__Graph  import Domain__Mermaid__Graph

class MGraph__Mermaid(MGraph):
    graph: Domain__Mermaid__Graph

    def code(self) -> str:
        return self.render().code()

    def edit(self) -> Mermaid__Edit:
        return Mermaid__Edit(graph=self.graph)

    def render(self) -> Mermaid__Render:
        return Mermaid__Render(graph=self.graph)