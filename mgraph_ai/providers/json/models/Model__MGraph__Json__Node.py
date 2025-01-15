from typing                                             import Any
from osbot_utils.type_safe.methods.type_safe_property   import set_as_property
from mgraph_ai.mgraph.models.Model__MGraph__Node        import Model__MGraph__Node

from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node import (
    Schema__MGraph__Json__Node,
    Schema__MGraph__Json__Node__Value,
    Schema__MGraph__Json__Node__Dict,
    Schema__MGraph__Json__Node__List,
    Schema__MGraph__Json__Node__Property,
)

class Model__MGraph__Json__Node(Model__MGraph__Node):                                       # Base model class for JSON nodes
    data: Schema__MGraph__Json__Node

class Model__MGraph__Json__Node__Value(Model__MGraph__Json__Node):                         # Model class for JSON value nodes
    data: Schema__MGraph__Json__Node__Value

    value_type = set_as_property('data.node_data', 'value_type')

    def is_primitive(self) -> bool:                                                         # Check if the value is a primitive type
        return self.value_type in (str, int, float, bool, type(None))

    @property
    def value(self) -> Any:
        return self.data.node_data.value

    @value.setter
    def value(self, new_value: Any) -> None:
        self.data.node_data.value      = new_value
        self.data.node_data.value_type = type(new_value)

class Model__MGraph__Json__Node__Dict(Model__MGraph__Json__Node):                          # Model class for JSON object nodes
    data: Schema__MGraph__Json__Node__Dict

class Model__MGraph__Json__Node__List(Model__MGraph__Json__Node):                          # Model class for JSON array nodes
    data: Schema__MGraph__Json__Node__List

class Model__MGraph__Json__Node__Property(Model__MGraph__Json__Node):                      # Model class for JSON object property nodes
    data: Schema__MGraph__Json__Node__Property

    name = set_as_property('data.node_data', 'name')