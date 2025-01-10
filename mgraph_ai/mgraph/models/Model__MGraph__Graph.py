from typing                                                 import Any, Type, Dict, List
from osbot_utils.helpers.Random_Guid                        import Random_Guid
from mgraph_ai.mgraph.models.Model__MGraph__Edge            import Model__MGraph__Edge
from mgraph_ai.mgraph.models.Model__MGraph__Node            import Model__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute     import Schema__MGraph__Attribute
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph         import Schema__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node          import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge          import Schema__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Config  import Schema__MGraph__Node__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config  import Schema__MGraph__Edge__Config
from osbot_utils.type_safe.Type_Safe                        import Type_Safe
from osbot_utils.type_safe.decorators.type_safe             import type_safe


class Model__MGraph__Graph(Type_Safe):
    data           : Schema__MGraph__Graph
    node_model_type: Type[Model__MGraph__Node]
    edge_model_type: Type[Model__MGraph__Edge]

    @type_safe
    def add_node(self, node: Schema__MGraph__Node) -> Model__MGraph__Node:                            # Add a node to the graph
        self.data.nodes[node.node_config.node_id] = node
        return self.node_model_type(data=node)

    @type_safe
    def add_edge(self, edge: Schema__MGraph__Edge) -> Model__MGraph__Edge:                            # Add an edge to the graph
        if edge.from_node_id not in self.data.nodes:
            raise ValueError(f"Source node {edge.from_node_id} not found")
        if edge.to_node_id not in self.data.nodes:
            raise ValueError(f"Target node {edge.to_node_id} not found")

        self.data.edges[edge.edge_config.edge_id] = edge
        return self.edge_model_type(data=edge)

    @type_safe
    def new_node(self, value     : Any                                                ,
                       node_type : Type[Schema__MGraph__Node                  ] = None,
                       attributes: Dict[Random_Guid, Schema__MGraph__Attribute] = None) -> Model__MGraph__Node:         # Create and add a new node to the graph

        if node_type is None:
            node_type = self.data.default_types.node_type or Schema__MGraph__Node
        config_type = self.data.default_types.node_config_type or Schema__MGraph__Node__Config

        node_config = config_type(value_type  = type(value))
        node        = node_type  (attributes  = attributes   ,
                                  node_config = node_config  ,
                                  node_type   = node_type    ,
                                  value       = value        )

        return self.add_node(node)

    @type_safe
    def new_edge(self, from_node_id: Random_Guid,
                       to_node_id  : Random_Guid,
                       attributes  : Dict[Random_Guid, Schema__MGraph__Attribute] = None) -> Model__MGraph__Edge:                                               # Create and add a new edge between nodes

        from_node = self.data.nodes.get(from_node_id)
        to_node   = self.data.nodes.get(to_node_id  )
        if from_node is None:
            raise ValueError(f"From node {from_node_id} not found")
        if to_node is None:
            raise ValueError(f"To node {to_node_id} not found")

        edge_type   = self.data.default_types.edge_type        or Schema__MGraph__Edge
        config_type = self.data.default_types.edge_config_type or Schema__MGraph__Edge__Config

        edge_config = config_type(edge_id        = Random_Guid(),
                                  from_node_type = self.data.nodes[from_node_id].node_type,
                                  to_node_type   = self.data.nodes[to_node_id  ].node_type)
        edge        = edge_type  (attributes     = attributes                               ,
                                  edge_config    = edge_config                              ,
                                  from_node_id   = from_node_id                             ,
                                  to_node_id     = to_node_id                               )

        return self.add_edge(edge)

    def edges(self):
        return [self.edge_model_type(data=data) for data in self.data.edges.values()]

    def edge(self, edge_id: Random_Guid) -> Model__MGraph__Edge:
        data = self.data.edges.get(edge_id)
        if data:
            return self.edge_model_type(data=data)

    def graph(self):
        return self.data

    def node(self, node_id: Random_Guid) -> Model__MGraph__Node:
        data = self.data.nodes.get(node_id)
        if data:
            return self.node_model_type(data=data)

    def nodes(self) -> List[Model__MGraph__Node]:
        return [self.node_model_type(data=node) for node in self.data.nodes.values()]

    @type_safe
    def delete_node(self, node_id: Random_Guid) -> 'Model__MGraph__Graph':                              # Remove a node and all its connected edges
        if node_id not in self.data.nodes:
            return False

        edges_to_remove = []                                                                            # Remove all edges connected to this node
        for edge_id, edge in self.data.edges.items():
            if edge.from_node_id == node_id or edge.to_node_id == node_id:
                edges_to_remove.append(edge_id)

        for edge_id in edges_to_remove:
            del self.data.edges[edge_id]

        del self.data.nodes[node_id]
        return True

    @type_safe
    def delete_edge(self, edge_id: Random_Guid) -> 'Model__MGraph__Graph':                              # Remove an edge from the graph
        if edge_id not in self.data.edges:
            return False

        del self.data.edges[edge_id]
        return True