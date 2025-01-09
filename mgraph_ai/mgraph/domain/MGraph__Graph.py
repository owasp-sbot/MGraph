from typing                                             import Any, Type, Dict, List
from mgraph_ai.mgraph.models.Model__MGraph__Edge        import Model__MGraph__Edge
from mgraph_ai.mgraph.models.Model__MGraph__Node        import Model__MGraph__Node
from osbot_utils.helpers.Random_Guid                    import Random_Guid
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute import Schema__MGraph__Attribute
from mgraph_ai.mgraph.domain.MGraph__Edge               import MGraph__Edge
from mgraph_ai.mgraph.domain.MGraph__Node               import MGraph__Node
from mgraph_ai.mgraph.models.Model__MGraph__Graph       import Model__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node      import Schema__MGraph__Node
from osbot_utils.type_safe.Type_Safe                    import Type_Safe


class MGraph__Graph(Type_Safe):
    model: Model__MGraph__Graph

    def delete_edge(self, edge_id: Random_Guid) -> bool:
        return self.model.delete_edge(edge_id)

    def delete_node(self, node_id: Random_Guid) -> bool:
        return self.model.delete_node(node_id)

    def edge(self, edge_id: Random_Guid) -> MGraph__Edge:
        edge = self.model.edge(edge_id)
        if edge:
            return self.mgraph_edge(edge=edge)

    def edges(self) -> List[MGraph__Edge]:
        return [self.mgraph_edge(edge=edge) for edge in self.model.edges()]

    def mgraph_edge(self, edge: Model__MGraph__Edge) -> MGraph__Edge:
        #edge_domain_type = self.model.default_types.node_domain_type           # todo: find way to do this
        edge_domain_type = MGraph__Edge
        return edge_domain_type(edge=edge, graph=self.model)

    def mgraph_node(self, node: Model__MGraph__Node) -> MGraph__Edge:
        #node_domain_type = self.model.default_types.node_domain_type           # todo: find way to do this
        node_domain_type = MGraph__Node
        return node_domain_type(node=node, graph=self.model)

    def new_edge(self, from_node_id: Random_Guid, to_node_id  : Random_Guid) -> MGraph__Edge:
        edge = self.model.new_edge(from_node_id=from_node_id, to_node_id=to_node_id)
        return self.mgraph_edge(edge=edge)

    def new_node(self, value     : Any                                                ,
                       node_type : Type[Schema__MGraph__Node                  ] = None,
                       attributes: Dict[Random_Guid, Schema__MGraph__Attribute] = None)-> MGraph__Node:
        node = self.model.new_node(value=value, node_type=node_type, attributes=attributes)
        return self.mgraph_node(node=node)

    def node(self, node_id: Random_Guid) -> MGraph__Node:
        node = self.model.node(node_id)
        if node:
            return self.mgraph_node(node=node)

    def nodes(self) -> List[MGraph__Node]:
        return [self.mgraph_node(node=node) for node in self.model.nodes()]

