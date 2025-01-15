from osbot_utils.type_safe.methods.type_safe_property           import set_as_property
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node import Domain__MGraph__Json__Node
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node  import Model__MGraph__Json__Node__Property



class Domain__MGraph__Json__Node__Property(Domain__MGraph__Json__Node):
    node : Model__MGraph__Json__Node__Property                                                    # Reference to property node model

    name = set_as_property('node', 'name')                                                       # Property name