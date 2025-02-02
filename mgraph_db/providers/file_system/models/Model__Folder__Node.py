from mgraph_db.providers.file_system.models.Model__File_System__Item import Model__File_System__Item
from mgraph_db.providers.file_system.schemas.Schema__Folder__Node    import Schema__Folder__Node

class Model__Folder__Node(Model__File_System__Item):                                                     # Model for folder nodes
    data: Schema__Folder__Node
