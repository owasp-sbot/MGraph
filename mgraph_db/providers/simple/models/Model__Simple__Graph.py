from mgraph_db.mgraph.models.Model__MGraph__Graph             import Model__MGraph__Graph
from mgraph_db.providers.simple.models.Model__Simple__Types   import Model__Simple__Types
from mgraph_db.providers.simple.schemas.Schema__Simple__Graph import Schema__Simple__Graph


class Model__Simple__Graph(Model__MGraph__Graph):
    data       : Schema__Simple__Graph
    model_types: Model__Simple__Types