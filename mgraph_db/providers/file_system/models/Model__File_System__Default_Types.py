from typing                                                     import Type
from mgraph_db.mgraph.models.Model__MGraph__Types      import Model__MGraph__Types
from mgraph_db.providers.file_system.models.Model__Folder__Node import Model__Folder__Node

class Model__File_System__Default_Types(Model__MGraph__Types):
    node_model_type: Type[Model__Folder__Node]