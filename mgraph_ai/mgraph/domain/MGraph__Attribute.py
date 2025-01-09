from typing                                           import Any
from osbot_utils.helpers.Random_Guid                  import Random_Guid
from mgraph_ai.mgraph.models.Model__MGraph__Attribute import Model__MGraph__Attribute
from mgraph_ai.mgraph.models.Model__MGraph__Graph     import Model__MGraph__Graph
from osbot_utils.type_safe.Type_Safe                  import Type_Safe

class MGraph__Attribute(Type_Safe):                                                        # Domain class for attributes
    attribute: Model__MGraph__Attribute                                                    # Reference to attribute model
    graph    : Model__MGraph__Graph                                                        # Reference to graph model

    def id(self) -> Random_Guid:                                                           # Get attribute ID
        return self.attribute.data.attribute_id

    def name(self) -> str:                                                                 # Get attribute name
        return str(self.attribute.data.attribute_name)

    def value(self) -> Any:                                                                # Get attribute value
        return self.attribute.value()

    def set_value(self, value: Any) -> 'MGraph__Attribute':                               # Set attribute value with type checking
        self.attribute.set_value(value)
        return self