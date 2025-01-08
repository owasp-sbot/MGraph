from osbot_utils.type_safe.Type_Safe             import Type_Safe
from osbot_utils.helpers.Random_Guid             import Random_Guid
from mgraph_ai.schemas.Schema__MGraph__Node      import Schema__MGraph__Node
from mgraph_ai.schemas.Schema__MGraph__Attribute import Schema__MGraph__Attribute

class Model__MGraph__Node(Type_Safe):
    data: Schema__MGraph__Node

    def value(self):
        return self.data.value

    def set_value(self, value):
        if self.data.node_config.value_type:
            if not isinstance(value, self.data.node_config.value_type):
                raise TypeError(f"Value must be of type {self.data.node_config.value_type}")
        self.data.value = value
        return self

    def add_attribute(self, attribute: Schema__MGraph__Attribute):
        self.data.attributes[attribute.attribute_id] = attribute
        return self

    def get_attribute(self, attribute_id: Random_Guid) -> Schema__MGraph__Attribute:
        return self.data.attributes.get(attribute_id)