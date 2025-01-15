from typing                                                             import Optional
from mgraph_ai.mgraph.domain.Domain__MGraph__Node                       import Domain__MGraph__Node
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node          import Model__MGraph__Json__Node
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__Dict  import Schema__MGraph__Json__Node__Dict
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__List  import Schema__MGraph__Json__Node__List
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__Value import Schema__MGraph__Json__Node__Value


class Domain__MGraph__Json__Node(Domain__MGraph__Node):
    node: Model__MGraph__Json__Node                                                              # Reference to node model

    def get_type(self) -> Optional[str]:                                                        # Get node type
        """Get the type of this JSON node (dict, list, or value)"""
        node_type = self.node.data.node_type
        if node_type == Schema__MGraph__Json__Node__Dict:
            return 'dict'
        elif node_type == Schema__MGraph__Json__Node__List:
            return 'list'
        elif node_type == Schema__MGraph__Json__Node__Value:
            return 'value'
        return None