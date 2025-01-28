from typing                                                      import Type
from mgraph_ai.mgraph.MGraph                                     import MGraph
from mgraph_ai.providers.json.actions.MGraph__Json__Export       import MGraph__Json__Export
from mgraph_ai.providers.json.actions.MGraph__Json__Load         import MGraph__Json__Load
from mgraph_ai.providers.json.actions.MGraph__Json__Query        import MGraph__Json__Query
from mgraph_ai.providers.json.actions.MGraph__Json__Screenshot   import MGraph__Json__Screenshot
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Graph import Domain__MGraph__Json__Graph


class MGraph__Json(MGraph):                                                                                          # Main JSON graph manager
    graph       : Domain__MGraph__Json__Graph
    query_class : Type[MGraph__Json__Query]

    def export    (self) -> MGraph__Json__Export    : return MGraph__Json__Export    (graph=self.graph)                 # Access export operations
    def load      (self) -> MGraph__Json__Load      : return MGraph__Json__Load      (graph=self.graph)                 # Access import operations
    def screenshot(self) -> MGraph__Json__Screenshot: return MGraph__Json__Screenshot(graph=self.graph)                 # Access screenshot operations
