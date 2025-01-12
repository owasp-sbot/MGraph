from typing                                                             import Type
from mgraph_ai.providers.file_system.domain.Folder__Node                import Folder__Node
from mgraph_ai.providers.file_system.models.Model__File_System__Graph   import Model__File_System__Graph
from mgraph_ai.providers.file_system.models.Model__Folder__Node         import Model__Folder__Node
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe

class File_System__Graph(Type_Safe):                                                                     # Domain class for filesystem graph
    model: Model__File_System__Graph
    node_model_type: Type[Model__Folder__Node]

    def allow_circular_refs(self) -> bool:                                                               # Check if circular refs allowed
        return self.model.allow_circular_refs()

    def set_allow_circular_refs(self, value: bool) -> 'File_System__Graph':                             # Set circular refs policy
        self.model.set_allow_circular_refs(value)
        return self

    def root_folder(self) -> Folder__Node:                                                               # Get root folder
        # Find node with no parent
        for node in self.model.nodes():
            has_parent = False
            for edge in self.model.edges():
                if edge.to_node_id == node.node_id():
                    has_parent = True
                    break
            if not has_parent:
                return Folder__Node(item=node, graph=self.model)
        return None