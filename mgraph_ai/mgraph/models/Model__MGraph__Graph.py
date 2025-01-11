from typing                                                 import Type, List
from osbot_utils.helpers.Random_Guid                        import Random_Guid
from mgraph_ai.mgraph.models.Model__MGraph__Edge            import Model__MGraph__Edge
from mgraph_ai.mgraph.models.Model__MGraph__Node            import Model__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph         import Schema__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node          import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge          import Schema__MGraph__Edge
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
            raise ValueError(f"From node {edge.from_node_id} not found")
        if edge.to_node_id not in self.data.nodes:
            raise ValueError(f"To node {edge.to_node_id} not found")

        self.data.edges[edge.edge_config.edge_id] = edge
        return self.edge_model_type(data=edge)

    def new_edge(self, **kwargs) -> Model__MGraph__Edge:
        edge_type = self.data.default_types.edge_type
        edge      = edge_type(**kwargs)
        return self.add_edge(edge)

    def new_node(self, **kwargs):
        node_type = self.data.default_types.node_type
        node      = node_type(**kwargs)
        return self.add_node(node)

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