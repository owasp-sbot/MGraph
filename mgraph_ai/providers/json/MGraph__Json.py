from mgraph_ai.mgraph.actions.MGraph__Data                       import MGraph__Data
from mgraph_ai.mgraph.actions.MGraph__Edit                       import MGraph__Edit
from mgraph_ai.mgraph.actions.MGraph__Storage                    import MGraph__Storage
from mgraph_ai.providers.json.actions.MGraph__Json__Export       import MGraph__Json__Export
from mgraph_ai.providers.json.actions.MGraph__Json__Load         import MGraph__Json__Load
from mgraph_ai.providers.json.actions.MGraph__Json__Screenshot   import MGraph__Json__Screenshot
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Graph import Domain__MGraph__Json__Graph
from osbot_utils.type_safe.Type_Safe                             import Type_Safe


class MGraph__Json(Type_Safe):                                                                                          # Main JSON graph manager
    graph : Domain__MGraph__Json__Graph

    def data      (self) -> MGraph__Data            : return MGraph__Data            (graph=self.graph)                 # Access data operations
    def edit      (self) -> MGraph__Edit            : return MGraph__Edit            (graph=self.graph)                 # Access edit operations
    def export    (self) -> MGraph__Json__Export    : return MGraph__Json__Export    (graph=self.graph)                 # Access export operations
    def load      (self) -> MGraph__Json__Load      : return MGraph__Json__Load      (graph=self.graph)                 # Access import operations
    def screenshot(self) -> MGraph__Json__Screenshot: return MGraph__Json__Screenshot(graph=self.graph)                 # Access screenshot operations
    def storage   (self) -> MGraph__Storage         : return MGraph__Storage         (graph=self.graph)                 # Access storage operations
