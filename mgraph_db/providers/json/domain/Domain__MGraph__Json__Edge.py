from mgraph_db.mgraph.domain.Domain__MGraph__Edge import Domain__MGraph__Edge
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node import Domain__MGraph__Json__Node


class Domain__MGraph__Json__Edge(Domain__MGraph__Edge):

    def from_node(self,**kwargs) -> Domain__MGraph__Json__Node:                                                        # Get source node
        return super().from_node(domain_node_type=Domain__MGraph__Json__Node)

    def to_node(self,**kwargs) -> Domain__MGraph__Json__Node:                                                        # Get source node
        return super().to_node(domain_node_type=Domain__MGraph__Json__Node)