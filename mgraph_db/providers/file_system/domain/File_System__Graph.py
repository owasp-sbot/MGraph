from typing                                                             import Type, Optional, List
from mgraph_db.providers.file_system.domain.Folder__Node                import Folder__Node
from mgraph_db.providers.file_system.models.Model__File_System__Graph   import Model__File_System__Graph
from mgraph_db.providers.file_system.models.Model__Folder__Node         import Model__Folder__Node
from mgraph_db.providers.file_system.actions.File_System__Data          import File_System__Data
from mgraph_db.providers.file_system.actions.File_System__Edit          import File_System__Edit
from mgraph_db.providers.file_system.actions.File_System__Filter        import File_System__Filter
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe

class File_System__Graph(Type_Safe):
    model          : Model__File_System__Graph
    node_model_type: Type[Model__Folder__Node]

    def data(self) -> File_System__Data:
        return File_System__Data(graph=self.model)

    def edit(self) -> File_System__Edit:
        return File_System__Edit(graph=self.model)

    def filter(self) -> File_System__Filter:
        return File_System__Filter(graph=self.model)

    # Convenience proxy methods
    def folder(self, path: str) -> Optional[Folder__Node]:
        return self.data().folder(path)

    def exists(self, path: str) -> bool:
        return self.data().exists(path)

    def root(self) -> Optional[Folder__Node]:
        return self.data().root()

    def find(self, pattern: str) -> List[Folder__Node]:
        return self.filter().find(pattern)