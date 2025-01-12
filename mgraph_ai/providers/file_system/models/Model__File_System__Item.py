from mgraph_ai.mgraph.models.Model__MGraph__Node                        import Model__MGraph__Node
from mgraph_ai.providers.file_system.schemas.Schema__File_System__Item  import Schema__File_System__Item

class Model__File_System__Item(Model__MGraph__Node):                                                      # Base model for filesystem items
    data: Schema__File_System__Item

    def folder_name(self) -> str:                                                                         # Get folder name
        return self.data.folder_name

    def set_folder_name(self, name: str) -> 'Model__File_System__Item':                                  # Set folder name
        self.data.folder_name = name
        return self

    def created_at(self):                                                                                # Get creation timestamp
        return self.data.created_at

    def modified_at(self):                                                                               # Get modification timestamp
        return self.data.modified_at

    def set_modified_at(self, value) -> 'Model__File_System__Item':                                      # Set modification timestamp
        self.data.modified_at = value
        return self


