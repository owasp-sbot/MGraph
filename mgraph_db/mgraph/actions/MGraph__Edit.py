from typing import Type

from mgraph_db.mgraph.actions.MGraph__Data          import MGraph__Data
from mgraph_db.mgraph.actions.MGraph__Index         import MGraph__Index
from mgraph_db.mgraph.domain.Domain__MGraph__Edge   import Domain__MGraph__Edge
from mgraph_db.mgraph.domain.Domain__MGraph__Graph  import Domain__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge  import Schema__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Node  import Schema__MGraph__Node
from osbot_utils.decorators.methods.cache_on_self   import cache_on_self
from osbot_utils.helpers.Obj_Id                     import Obj_Id
from osbot_utils.type_safe.Type_Safe                import Type_Safe


class MGraph__Edit(Type_Safe):
    graph    : Domain__MGraph__Graph
    data_type: Type[MGraph__Data]

    def add_node(self, node: Schema__MGraph__Node):
        with self.index() as index:                                     # used context here so that we have an index object in the state before we add a node (or the node data will be loaded twice)
            result = self.graph.add_node(node)                          # Add node to graph
            index.add_node(node)                                        # Add to index
        return result

    def add_edge(self, edge: Schema__MGraph__Edge):
        result = self.graph.add_edge(edge)                               # Add edge to graph
        self.index().add_edge(edge)                                      # Add to index
        return result

    def new_node(self, **kwargs):
        with self.index() as index:
            node = self.graph.new_node(**kwargs)                             # Create new node
            index.add_node(node.node.data)                           # Add to index
        return node

    def new_edge(self, **kwargs) -> Domain__MGraph__Edge:                # Add a new edge between nodes
        edge = self.graph.new_edge(**kwargs)                             # Create new edge
        self.index().add_edge(edge.edge.data)                           # Add to index
        return edge

    def delete_node(self, node_id: Obj_Id) -> bool:                      # Remove a node and its connected edges
        node = self.data().node(node_id)
        if node:
            self.index().remove_node(node.node.data)                     # Remove from index first
        return self.graph.delete_node(node_id)

    def delete_edge(self, edge_id: Obj_Id) -> bool:                      # Remove an edge
        edge = self.data().edge(edge_id)
        if edge:
            self.index().remove_edge(edge.edge.data)                     # Remove from index first
        return self.graph.delete_edge(edge_id)

    @cache_on_self
    def data(self):
        return self.data_type(graph=self.graph)

    @cache_on_self
    def index(self) -> MGraph__Index:                                    # Cached access to index
        return MGraph__Index.from_graph(self.graph)