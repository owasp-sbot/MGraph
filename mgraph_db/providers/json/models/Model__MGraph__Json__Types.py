from typing                                                     import Type
from mgraph_db.providers.json.models.Model__MGraph__Json__Edge  import Model__MGraph__Json__Edge
from mgraph_db.providers.json.models.Model__MGraph__Json__Node  import Model__MGraph__Json__Node
from osbot_utils.type_safe.Type_Safe                            import Type_Safe

class Model__MGraph__Json__Types(Type_Safe):
    node_model_type: Type[Model__MGraph__Json__Node]
    edge_model_type: Type[Model__MGraph__Json__Edge]

    def __init__(self, **kwargs):
        node_model_type = kwargs.get('node_model_type') or self.__annotations__['node_model_type'].__args__[0]
        edge_model_type = kwargs.get('edge_model_type') or self.__annotations__['edge_model_type'].__args__[0]

        types_dict = dict(node_model_type = node_model_type,
                          edge_model_type = edge_model_type)
        object.__setattr__(self, '__dict__', types_dict)