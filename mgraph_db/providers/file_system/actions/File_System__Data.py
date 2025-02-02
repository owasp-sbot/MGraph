from typing                                                           import Optional
from mgraph_db.providers.file_system.domain.Folder__Node                import Folder__Node
from mgraph_db.providers.file_system.models.Model__File_System__Graph   import Model__File_System__Graph
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe

class File_System__Data(Type_Safe):
    graph: Model__File_System__Graph

    def folder(self, path: str) -> Optional[Folder__Node]:                                              # Get folder by path
        if not path:
            return None
        parts = path.strip('/').split('/')
        current = self.root()

        if not current:                                                                                  # No root exists
            return None

        if len(parts) == 1 and not parts[0]:                                                            # Root path "/"
            return current

        for part in parts:
            if not current:
                return None
            current = self.child_by_name(current, part)
        return current

    def child_by_name(self, parent: Folder__Node, name: str) -> Optional[Folder__Node]:                 # Get child by name
        for edge in self.graph.edges():
            if edge.from_node_id == parent.node_id:
                child = self.graph.node(edge.to_node_id)
                if child and child.folder_name == name:
                    return Folder__Node(item=child, graph=self.graph)
        return None

    def exists(self, path: str) -> bool:                                                                # Check if path exists
        return self.folder(path) is not None

    def root(self) -> Optional[Folder__Node]:                                                           # Get root folder
        for node in self.graph.nodes():
            has_parent = False
            for edge in self.graph.edges():
                if edge.to_node_id == node.node_id:
                    has_parent = True
                    break
            if not has_parent:
                return Folder__Node(item=node, graph=self.graph)
        return None