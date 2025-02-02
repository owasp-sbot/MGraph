from typing                                                 import Type
from mgraph_ai.mgraph.models.Model__MGraph__Edge            import Model__MGraph__Edge
from mgraph_ai.mgraph.models.Model__MGraph__Types           import Model__MGraph__Types
from mgraph_ai.providers.simple.models.Model__Simple__Node  import Model__Simple__Node


class Model__Simple__Types(Model__MGraph__Types):
    node_model_type: Type[Model__Simple__Node]
    edge_model_type: Type[Model__MGraph__Edge]