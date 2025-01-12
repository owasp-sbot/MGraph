from typing                                                           import List
from mgraph_ai.providers.file_system.domain.File_System__Item         import File_System__Item
from mgraph_ai.providers.file_system.models.Model__File_System__Graph import Model__File_System__Graph
from mgraph_ai.providers.file_system.models.Model__Folder__Node       import Model__Folder__Node


class Folder__Node(File_System__Item):                                                                   # Domain class for folder nodes
    item : Model__Folder__Node
    graph: Model__File_System__Graph

    def children(self) -> List['Folder__Node']:                                                          # Get child folders
        children = []
        for edge in self.graph.edges():
            if edge.from_node_id == self.item.node_id():
                child = self.graph.node(edge.to_node_id)
                if child:
                    children.append(Folder__Node(item=child, graph=self.graph))
        return children

    def parent(self) -> 'Folder__Node':                                                                  # Get parent folder
        for edge in self.graph.edges():
            if edge.to_node_id == self.item.node_id():
                parent = self.graph.node(edge.from_node_id)
                if parent:
                    return Folder__Node(item=parent, graph=self.graph)
        return None