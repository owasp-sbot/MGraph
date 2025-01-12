from typing                                                           import List, Type
from mgraph_ai.providers.file_system.models.Model__File_System__Graph import Model__File_System__Graph
from mgraph_ai.providers.file_system.models.Model__File_System__Item  import Model__File_System__Item
from osbot_utils.type_safe.Type_Safe                                  import Type_Safe


class File_System__Item(Type_Safe):                                                                      # Base domain class for filesystem items
    item : Model__File_System__Item
    graph: Model__File_System__Graph

    def folder_name(self) -> str:                                                                        # Get folder name
        return self.item.folder_name()

    def set_folder_name(self, name: str) -> 'File_System__Item':                                        # Set folder name
        self.item.set_folder_name(name)
        return self

    def created_at(self):                                                                               # Get creation timestamp
        return self.item.created_at()

    def modified_at(self):                                                                              # Get modification timestamp
        return self.item.modified_at()

    def update_modified_at(self):                                                                       # Update modification timestamp
        self.item.update_modified_at()
        return self

    def path(self) -> List[str]:                                                                        # Get full path
        path_parts = []
        current_id = self.item.node_id()
        visited = set()

        while current_id and current_id not in visited:
            visited.add(current_id)
            current_node = self.graph.node(current_id)
            if not current_node:
                break
            path_parts.append(current_node.folder_name())

            # Find parent folder
            parent_edge = None
            for edge in self.graph.edges():
                if edge.to_node_id == current_id:
                    parent_edge = edge
                    break

            current_id = parent_edge.from_node_id if parent_edge else None

        return list(reversed(path_parts))

