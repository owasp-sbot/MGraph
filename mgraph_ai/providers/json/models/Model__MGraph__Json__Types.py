from typing                                                     import Type
from mgraph_ai.providers.json.models.Model__MGraph__Json__Edge  import Model__MGraph__Json__Edge
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node  import Model__MGraph__Json__Node
from osbot_utils.type_safe.Type_Safe                            import Type_Safe

class Model__MGraph__Json__Types(Type_Safe):
    node_model_type: Type[Model__MGraph__Json__Node]
    edge_model_type: Type[Model__MGraph__Json__Edge]