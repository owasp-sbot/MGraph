from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph                     import Schema__MGraph__Graph
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Graph__Data import Schema__MGraph__Json__Graph__Data
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Types       import Schema__MGraph__Json__Types


class Schema__MGraph__Json__Graph(Schema__MGraph__Graph):
    schema_types : Schema__MGraph__Json__Types
    graph_data   : Schema__MGraph__Json__Graph__Data