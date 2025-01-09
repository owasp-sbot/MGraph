from mgraph_ai.mgraph.domain.MGraph__Graph  import MGraph__Graph
from osbot_utils.type_safe.Type_Safe        import Type_Safe

class MGraph__Storage(Type_Safe):
    graph: MGraph__Graph

    def create(self) -> MGraph__Graph:                       # overwrite on classes that have a storage target
        self.graph = MGraph__Graph()
        return self.graph

    def delete(self) -> bool:                       # overwrite on classes that have a storage target
        raise NotImplementedError('delete applicable to memory only mode')

    def safe(self) -> bool:                         # overwrite on classes that have a storage target
        return True                         # default is to memory, so that it is already saved