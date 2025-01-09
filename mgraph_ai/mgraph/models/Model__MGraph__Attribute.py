from osbot_utils.type_safe.Type_Safe                    import Type_Safe
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute import Schema__MGraph__Attribute

class Model__MGraph__Attribute(Type_Safe):
    data: Schema__MGraph__Attribute

    def value(self):
        return self.data.attribute_value

    def set_value(self, value):
        if self.data.attribute_type:
            if not isinstance(value, self.data.attribute_type):
                raise TypeError(f"Value must be of type {self.data.attribute_type}")
        self.data.attribute_value = value
        return self