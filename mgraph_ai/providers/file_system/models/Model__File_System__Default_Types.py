from typing                                                     import Type
from mgraph_ai.mgraph.models.Model__MGraph__Default__Types      import Model__MGraph__Default__Types
from mgraph_ai.providers.file_system.models.Model__Folder__Node import Model__Folder__Node

class Model__File_System__Default_Types(Model__MGraph__Default__Types):
    node_model_type: Type[Model__Folder__Node]