from typing                                                           import List
from fnmatch                                                         import fnmatch
from mgraph_db.providers.file_system.domain.Folder__Node                import Folder__Node
from mgraph_db.providers.file_system.models.Model__File_System__Graph   import Model__File_System__Graph
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe

class File_System__Filter(Type_Safe):
    graph: Model__File_System__Graph

    def find(self, pattern: str) -> List[Folder__Node]:                                               # Find folders matching pattern
        results = []
        for node in self.graph.nodes():
            if fnmatch(node.folder_name(), pattern):
                results.append(Folder__Node(item=node, graph=self.graph))
        return results