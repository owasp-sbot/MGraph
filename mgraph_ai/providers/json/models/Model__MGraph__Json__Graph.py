from mgraph_ai.mgraph.models.Model__MGraph__Graph                 import Model__MGraph__Graph
from mgraph_ai.providers.json.models.Model__MGraph__Json__Types   import Model__MGraph__Json__Types
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Graph import Schema__MGraph__Json__Graph


class Model__MGraph__Json__Graph(Model__MGraph__Graph):
    data       : Schema__MGraph__Json__Graph
    model_types: Model__MGraph__Json__Types