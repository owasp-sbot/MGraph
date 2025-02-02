from typing                                                           import Optional
from mgraph_db.providers.file_system.domain.Folder__Node                import Folder__Node
from mgraph_db.providers.file_system.models.Model__File_System__Graph   import Model__File_System__Graph
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe

class File_System__Edit(Type_Safe):
    graph: Model__File_System__Graph

    def allow_circular_refs(self, value: bool) -> 'File_System__Edit':                                 # Set circular refs policy
        self.graph.set_allow_circular_refs(value)
        return self

    def set_root(self, folder: Folder__Node) -> 'File_System__Edit':                                  # Set root folder
        if len(self.graph.nodes()) > 0:
            raise ValueError("Cannot set root on non-empty graph")
        self.graph.add_node(folder.node.data)
        return self

    def add_folder(self, parent: Folder__Node, name: str) -> Folder__Node:                           # Add child folder
        if not parent or not name:
            raise ValueError("Parent and name are required")

        # Check for existing folder with same name
        for edge in self.graph.edges():
            if edge.from_node_id == parent.node_id:
                child = self.graph.node(edge.to_node_id)
                if child and child.folder_name() == name:
                    raise ValueError(f"Folder {name} already exists")

        # Create and add new folder
        folder = self.graph.new_node(folder_name=name)
        self.graph.new_edge(from_node_id=parent.node_id,
                           to_node_id=folder.node_id)

        return Folder__Node(item=folder, graph=self.graph)