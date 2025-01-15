from typing                                                      import Any
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node import Schema__MGraph__Json__Node
from mgraph_ai.mgraph.models.Model__MGraph__Node                 import Model__MGraph__Node

class Model__MGraph__Json__Node(Model__MGraph__Node):                                       # Base model class for JSON nodes
    data: Schema__MGraph__Json__Node

