from typing                                         import Any
from osbot_utils.type_safe.decorators.type_safe     import type_safe
from osbot_utils.type_safe.Type_Safe                import Type_Safe
from osbot_utils.helpers.Random_Guid                import Random_Guid
from mgraph_ai.schemas.Schema__MGraph__Graph        import Schema__MGraph__Graph
from mgraph_ai.schemas.Schema__MGraph__Node         import Schema__MGraph__Node
from mgraph_ai.schemas.Schema__MGraph__Edge         import Schema__MGraph__Edge
from mgraph_ai.schemas.Schema__MGraph__Node_Config  import Schema__MGraph__Node_Config
from mgraph_ai.schemas.Schema__MGraph__Edge_Config  import Schema__MGraph__Edge_Config

class Model__MGraph__Graph(Type_Safe):
    data: Schema__MGraph__Graph

    @type_safe
    def add_node(self, node: Schema__MGraph__Node) -> Schema__MGraph__Node:                           # Add a node to the graph
        self.data.nodes[node.node_config.node_id] = node
        return node

    @type_safe
    def add_edge(self, edge: Schema__MGraph__Edge) -> Schema__MGraph__Edge:                           # Add an edge to the graph
        if edge.from_node_id not in self.data.nodes:
            raise ValueError(f"Source node {edge.from_node_id} not found")
        if edge.to_node_id not in self.data.nodes:
            raise ValueError(f"Target node {edge.to_node_id} not found")

        self.data.edges[edge.edge_config.edge_id] = edge
        return edge

    @type_safe
    def new_node(self, value: Any, node_type: type = None, attributes=None) -> Schema__MGraph__Node:               # Create and add a new node to the graph
        if node_type is None:
            node_type = self.data.graph_config.default_node_type

        node_config = Schema__MGraph__Node_Config(node_id     = Random_Guid(),
                                                  value_type  = type(value)  )
        node        = Schema__MGraph__Node       (attributes  = attributes   ,
                                                  node_config = node_config  ,
                                                  node_type   = node_type    ,
                                                  value       = value        )

        return self.add_node(node)

    @type_safe
    def new_edge(self, from_node_id: Random_Guid, to_node_id: Random_Guid) -> Schema__MGraph__Edge: # Create and add a new edge between nodes"""
        from_node = self.data.nodes.get(from_node_id)
        to_node   = self.data.nodes.get(to_node_id  )
        if from_node is None:
            raise ValueError(f"Node {from_node_id} not found")
        if to_node is None:
            raise ValueError(f"Node {to_node_id} not found")
        edge_config = Schema__MGraph__Edge_Config(edge_id        = Random_Guid(),
                                                  from_node_type = self.data.nodes[from_node_id].node_type,
                                                  to_node_type   = self.data.nodes[to_node_id  ].node_type)

        edge = Schema__MGraph__Edge(attributes   = {}          ,
                                    edge_config  = edge_config ,
                                    from_node_id = from_node_id,
                                    to_node_id    =to_node_id  )

        return self.add_edge(edge)

    def edges(self):
        return self.data.edges.values()

    def get_node(self, node_id: Random_Guid) -> Schema__MGraph__Node:
        return self.data.nodes.get(node_id)

    def get_edge(self, edge_id: Random_Guid) -> Schema__MGraph__Edge:
        return self.data.edges.get(edge_id)

    def graph(self):
        return self.data

    def nodes(self):
        return self.data.nodes.values()

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