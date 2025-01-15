from osbot_utils.type_safe.methods.type_safe_property           import set_as_property
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node import Domain__MGraph__Json__Node
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node  import Model__MGraph__Json__Node__Value



class Domain__MGraph__Json__Node__Value(Domain__MGraph__Json__Node):
    node: Model__MGraph__Json__Node__Value                                                         # Reference to value node model

    value      = set_as_property('node', 'value'     )                                             # Value property
    value_type = set_as_property('node', 'value_type')                                             # Value type property

    def is_primitive(self) -> bool:                                                                # Check if value is a JSON primitive
        return self.node.is_primitive()