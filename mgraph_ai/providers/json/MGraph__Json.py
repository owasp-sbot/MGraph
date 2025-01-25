from mgraph_ai.mgraph.actions.MGraph__Data                                import MGraph__Data
from mgraph_ai.mgraph.actions.MGraph__Edit                                import MGraph__Edit
from mgraph_ai.mgraph.actions.MGraph__Storage                             import MGraph__Storage
from mgraph_ai.providers.json.actions.MGraph__Json__Export                import MGraph__Json__Export
from mgraph_ai.providers.json.actions.MGraph__Json__Load                  import MGraph__Json__Load
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Graph          import Domain__MGraph__Json__Graph
from osbot_utils.type_safe.Type_Safe                                      import Type_Safe


class MGraph__Json(Type_Safe):                                                                 # Main JSON graph manager
    graph : Domain__MGraph__Json__Graph

    def data(self) -> MGraph__Data:                                                           # Access data operations
        return MGraph__Data(graph=self.graph)

    def edit(self) -> MGraph__Edit:                                                           # Access edit operations
        return MGraph__Edit(graph=self.graph)

    def export(self) -> MGraph__Json__Export:                                                 # Access export operations
        return MGraph__Json__Export(graph=self.graph)

    def load(self) -> MGraph__Json__Load:                                                # Access import operations
        return MGraph__Json__Load(graph=self.graph)

    def storage(self) -> MGraph__Storage:                                                     # Access storage operations
        return MGraph__Storage(graph=self.graph)