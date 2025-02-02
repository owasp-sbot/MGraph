from mgraph_db.mgraph.domain.Domain__MGraph__Graph  import Domain__MGraph__Graph
from osbot_utils.type_safe.Type_Safe                import Type_Safe

class MGraph__Storage(Type_Safe):
    graph: Domain__MGraph__Graph

    def create(self) -> Domain__MGraph__Graph:                       # overwrite on classes that have a storage target
        self.graph = Domain__MGraph__Graph()
        return self.graph

    def delete(self) -> bool:                       # overwrite on classes that have a storage target
        raise NotImplementedError('delete applicable to memory only mode')

    def safe(self) -> bool:                         # overwrite on classes that have a storage target
        return True                         # default is to memory, so that it is already saved