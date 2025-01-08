from osbot_utils.type_safe.Type_Safe             import Type_Safe
from osbot_utils.helpers.Random_Guid             import Random_Guid
from mgraph_ai.schemas.Schema__MGraph__Edge      import Schema__MGraph__Edge
from mgraph_ai.schemas.Schema__MGraph__Attribute import Schema__MGraph__Attribute

class Model__MGraph__Edge(Type_Safe):
    data: Schema__MGraph__Edge

    def add_attribute(self, attribute: Schema__MGraph__Attribute):
        self.data.attributes[attribute.attribute_id] = attribute
        return self

    def get_attribute(self, attribute_id: Random_Guid) -> Schema__MGraph__Attribute:
        return self.data.attributes.get(attribute_id)

    def from_node_id(self) -> Random_Guid:
        return self.data.from_node_id

    def to_node_id(self) -> Random_Guid:
        return self.data.to_node_id