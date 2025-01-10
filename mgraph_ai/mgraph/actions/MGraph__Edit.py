from typing                                             import Any, Type, Dict
from mgraph_ai.mgraph.domain.MGraph__Edge               import MGraph__Edge
from mgraph_ai.mgraph.domain.MGraph__Graph              import MGraph__Graph
from mgraph_ai.mgraph.domain.MGraph__Node               import MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute import Schema__MGraph__Attribute
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node      import Schema__MGraph__Node
from osbot_utils.helpers.Random_Guid                    import Random_Guid
from osbot_utils.type_safe.Type_Safe                    import Type_Safe
from osbot_utils.type_safe.decorators.type_safe         import type_safe

class MGraph__Edit(Type_Safe):
    graph: MGraph__Graph

    def add_node(self, **kwargs):
        node_type   = self.graph.model.data.default_types.node_type
        domain_type = self.graph.node_domain_type
        node_data   = node_type(**kwargs)
        node        = self.graph.model.add_node(node_data)
        domain_type = domain_type(node=node, graph=self.graph.model)
        return domain_type

    @type_safe
    def new_node(self, value     : Any                                                ,
                       node_type : Type[Schema__MGraph__Node                  ] = None,
                       attributes: Dict[Random_Guid, Schema__MGraph__Attribute] = None) -> MGraph__Node:        # Add a new Node

        return self.graph.new_node(value=value, node_type=node_type, attributes=attributes)

    @type_safe
    def new_edge(self, from_node_id: Random_Guid,
                       to_node_id  : Random_Guid) -> MGraph__Edge:                                              # Add a new edge between nodes

        return self.graph.new_edge(from_node_id=from_node_id, to_node_id=to_node_id)

    def delete_node(self, node_id: Random_Guid) -> bool:                                                        # Remove a node and its connected edges
        return self.graph.delete_node(node_id)

    def delete_edge(self, edge_id: Random_Guid) -> bool:                                                        # Remove an edge
        return self.graph.delete_edge(edge_id)

