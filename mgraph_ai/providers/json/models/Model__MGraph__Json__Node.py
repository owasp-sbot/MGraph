from typing import Any, Type

from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node import Schema__MGraph__Json__Node, \
    Schema__MGraph__Json__Node__Type, Schema__MGraph__Json__Node__Dict, Schema__MGraph__Json__Node__List, \
    Schema__MGraph__Json__Node__Property, Schema__MGraph__Json__Node__Value
from mgraph_ai.mgraph.models.Model__MGraph__Node import Model__MGraph__Node


class Model__MGraph__Json__Node(Model__MGraph__Node):                                       # Base model class for JSON nodes
    data: Schema__MGraph__Json__Node

    def node_type(self) -> Schema__MGraph__Json__Node__Type:                        # Return the node's type
        return self.data.node_type if hasattr(self.data, 'node_type') else None

    def is_value(self) -> bool:                                                     # Check if node is a value type
        return self.node_type() == Schema__MGraph__Json__Node__Type.VALUE

    def is_dict(self) -> bool:                                                      # Check if node is a dictionary type
        return self.node_type() == Schema__MGraph__Json__Node__Type.DICT

    def is_list(self) -> bool:                                                      # Check if node is a list type
        return self.node_type() == Schema__MGraph__Json__Node__Type.LIST

    def is_property(self) -> bool:                                                  # Check if node is a property type
        return self.node_type() == Schema__MGraph__Json__Node__Type.PROPERTY

class Model__MGraph__Json__Node__Value(Model__MGraph__Json__Node):                                  # Model for JSON value nodes
    data: Schema__MGraph__Json__Node__Value

    def get_value(self) -> Any:                                                     # Retrieve the node's value
        return self.data.value

    def get_value_type(self) -> Type:                                               # Get the type of the value
        return self.data.value_type

    def set_value(self, value: Any):                                                # Set the node's value
        self.data.value = value
        self.data.value_type = type(value)

class Model__MGraph__Json__Node__Dict(Model__MGraph__Json__Node):                                   # Model for JSON dictionary nodes"""
    data: Schema__MGraph__Json__Node__Dict

    def keys(self):                                                                 # Placeholder for getting dictionary keys
        # This would likely be implemented in the domain layer
        return []

class Model__MGraph__Json__Node__List(Model__MGraph__Json__Node):                                   # Model for JSON list nodes"""
    data: Schema__MGraph__Json__Node__List

    def length(self) -> int:                                                        # Placeholder for getting list length
        # This would likely be implemented in the domain layer
        return 0

class Model__MGraph__Json__Node__Property(Model__MGraph__Json__Node):                               # Model for JSON property nodes"""
    data: Schema__MGraph__Json__Node__Property

    def get_name(self) -> str:                                                      # Get the property name
        return self.data.name

    def set_name(self, name: str):                                                  # Set the property name
        self.data.name = name