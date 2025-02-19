from typing                                                      import Type
from mgraph_db.mgraph.MGraph                                     import MGraph
from mgraph_db.providers.json.actions.MGraph__Json__Data         import MGraph__Json__Data
from mgraph_db.providers.json.actions.MGraph__Json__Export       import MGraph__Json__Export
from mgraph_db.providers.json.actions.MGraph__Json__Load         import MGraph__Json__Load
from mgraph_db.providers.json.actions.MGraph__Json__Query        import MGraph__Json__Query
from mgraph_db.providers.json.actions.MGraph__Json__Screenshot   import MGraph__Json__Screenshot
from mgraph_db.providers.json.actions.MGraph__Json__Edit         import MGraph__Json__Edit
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Graph import Domain__MGraph__Json__Graph


class MGraph__Json(MGraph):                                                                                          # Main JSON graph manager
    graph           : Domain__MGraph__Json__Graph
    query_class     : Type[MGraph__Json__Query     ]
    screenshot_class: Type[MGraph__Json__Screenshot]

    def data      (self) -> MGraph__Json__Data      : return MGraph__Json__Data      (graph=self.graph)
    def edit      (self) -> MGraph__Json__Edit      : return MGraph__Json__Edit      (graph=self.graph)
    def export    (self) -> MGraph__Json__Export    : return MGraph__Json__Export    (graph=self.graph)                 # Access export operations
    def load      (self) -> MGraph__Json__Load      : return MGraph__Json__Load      (graph=self.graph)                 # Access import operations
