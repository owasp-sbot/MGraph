from mgraph_db.mgraph.schemas.Schema__MGraph__Graph                              import Schema__MGraph__Graph
from mgraph_db.providers.file_system.schemas.Schema__File_System__Types          import Schema__File_System__Types
from mgraph_db.providers.file_system.schemas.Schema__File_System__Graph__Config  import Schema__File_System__Graph__Config


class Schema__File_System__Graph(Schema__MGraph__Graph):
    schema_types : Schema__File_System__Types
    graph_data   : Schema__File_System__Graph__Config