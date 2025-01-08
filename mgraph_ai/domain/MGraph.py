from osbot_utils.type_safe.Type_Safe        import Type_Safe
from mgraph_ai.actions.MGraph__Data         import MGraph__Data
from mgraph_ai.actions.MGraph__Edit         import MGraph__Edit
from mgraph_ai.actions.MGraph__Filter       import MGraph__Filter
from mgraph_ai.actions.MGraph__Storage      import MGraph__Storage
from mgraph_ai.models.Model__MGraph__Graph  import Model__MGraph__Graph

class MGraph(Type_Safe):                                                                                        # Main MGraph class that users will interact with
    graph: Model__MGraph__Graph                                                                                 # Reference to the underlying graph model

    def data(self) -> MGraph__Data:
        return MGraph__Data(graph=self.graph)

    def edit(self) -> MGraph__Edit:
        return MGraph__Edit(graph=self.graph)

    def storage(self) -> MGraph__Storage:
        return MGraph__Storage(graph=self.graph)

    def filter(self) -> MGraph__Filter:
        return MGraph__Filter(graph=self.graph)





