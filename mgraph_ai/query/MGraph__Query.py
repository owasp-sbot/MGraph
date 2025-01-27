from typing                                                 import Set, Dict, Any, Type, Optional, Callable, List
from mgraph_ai.mgraph.domain.Domain__MGraph__Node           import Domain__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge          import Schema__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node          import Schema__MGraph__Node
from mgraph_ai.query.models.Model__MGraph__Query__View      import Model__MGraph__Query__View
from mgraph_ai.query.models.Model__MGraph__Query__Views     import Model__MGraph__Query__Views
from osbot_utils.helpers.Obj_Id                             import Obj_Id
from mgraph_ai.mgraph.actions.MGraph__Data                  import MGraph__Data
from mgraph_ai.mgraph.index.MGraph__Index                   import MGraph__Index
from osbot_utils.type_safe.Type_Safe                        import Type_Safe
from osbot_utils.utils.Dev                                  import pprint

class MGraph__Query(Type_Safe):
    mgraph_data  : MGraph__Data
    mgraph_index : MGraph__Index
    query_views  : Model__MGraph__Query__Views

    def setup(self):
        source_nodes, source_edges = self.get_source_ids()              # get all the current nodes and edges
        self.create_view(nodes_ids = source_nodes,                      # create a view for it which is the initial view
                         edges_ids = source_edges,
                         operation = 'initial'   ,
                         params    = {}          )
        return self

    def reset(self):
        self.query_views = Model__MGraph__Query__Views()
        self.setup()
        return self
    def get_source_ids(self) -> tuple[Set[Obj_Id], Set[Obj_Id]]:
        return (set(self.mgraph_data.nodes_ids()),
                set(self.mgraph_data.edges_ids()))

    def get_current_ids(self) -> tuple[Set[Obj_Id], Set[Obj_Id]]:
        current_view = self.query_views.current_view()
        if not current_view:
            return self.get_source_ids()
        return (current_view.nodes_ids(),
                current_view.edges_ids())

    def get_connecting_edges(self, node_ids: Set[Obj_Id]) -> Set[Obj_Id]:
        edges = set()
        for node_id in node_ids:
            node           = self.mgraph_data.node(node_id)
            outgoing_edges = self.mgraph_index.get_node_outgoing_edges(node)
            incoming_edges = self.mgraph_index.get_node_incoming_edges(node)
            edges.update(outgoing_edges)
            edges.update(incoming_edges)
        return edges

    def create_view(self, nodes_ids: Set[Obj_Id],
                          edges_ids : Set[Obj_Id],
                          operation : str,
                          params    : Dict[str, Any]
                    )  -> Model__MGraph__Query__View:
        current_view = self.query_views.current_view()
        previous_id = current_view.view_id() if current_view else None

        return self.query_views.add_view(nodes_ids   = nodes_ids  ,
                                         edges_ids   = edges_ids  ,
                                         operation   = operation  ,
                                         params      = params     ,
                                         previous_id = previous_id)

    def by_type(self, node_type: Type[Schema__MGraph__Node]) -> 'MGraph__Query':
        matching_ids = self.mgraph_index.get_nodes_by_type(node_type)
        current_nodes, current_edges = self.get_current_ids()

        filtered_nodes = matching_ids & current_nodes if current_nodes else matching_ids
        filtered_edges = self.get_connecting_edges(filtered_nodes)

        self.create_view(nodes_ids = filtered_nodes,
                         edges_ids = filtered_edges,
                         operation = 'by_type',
                         params    = {'type': node_type.__name__})
        return self

    def go_back(self) -> bool:
        current_view = self.query_views.current_view()
        if current_view and current_view.previous_view_id():
            return self.query_views.set_current_view(current_view.previous_view_id())
        return False

    def go_forward(self, view_id: Optional[Obj_Id] = None) -> bool:
        current_view = self.query_views.current_view()
        if not current_view:
            return False

        next_ids = current_view.next_view_ids()
        if not next_ids:
            return False

        if view_id:
            if view_id in next_ids:
                return self.query_views.set_current_view(view_id)
            return False

        return self.query_views.set_current_view(next(iter(next_ids)))


    def with_field(self, name: str, value: Any) -> 'MGraph__Query':
        matching_ids = self.mgraph_index.get_nodes_by_field(name, value)

        current_nodes, current_edges = self.get_current_ids()

        filtered_nodes = matching_ids & current_nodes if current_nodes else matching_ids
        filtered_edges = self.get_connecting_edges(filtered_nodes)

        self.create_view(nodes_ids = filtered_nodes,
                         edges_ids = filtered_edges,
                         operation = 'with_field',
                         params    = {'name': name, 'value': value})
        return self

    def re_index(self):
        self.mgraph_index = MGraph__Index.from_graph(self.mgraph_data.graph)

    def collect(self) -> List[Domain__MGraph__Node]:                                                    #  Returns list of all matching nodes in current view"""
        nodes_ids    = self.get_current_ids()[0]
        return [self.mgraph_data.node(node_id)
                for node_id in nodes_ids]

    def first(self) -> Optional[Domain__MGraph__Node]:                                                  # Returns first matching node or None"""
        nodes_ids = self.get_current_ids()[0]
        if nodes_ids:
            return self.mgraph_data.node(next(iter(nodes_ids)))
        return None

    def value(self) -> Optional[Any]:                                                                   # Returns value of first matching node or None
        first_node = self.first()
        return first_node.node_data.value if first_node else None

    def count(self) -> int:                                                                             # Returns count of matching nodes
        return len(self.get_current_ids()[0])

    def exists(self) -> bool:                                                                           # Returns whether any nodes match current query
        return bool(self.get_current_ids()[0])

    def current_view(self) -> Optional[Model__MGraph__Query__View]:                                     # Returns current view if any
        return self.query_views.current_view()

    def traverse(self, edge_type: Optional[Type[Schema__MGraph__Edge]] = None) -> 'MGraph__Query':      # Traverses to connected nodes, optionally filtering by edge type"""
        current_nodes, _ = self.get_current_ids()
        connected_nodes = set()

        for node_id in current_nodes:
            # Get connecting edges
            edges = self.mgraph_index.get_node_outgoing_edges(
                self.mgraph_data.node(node_id))

            if edge_type:
                edges = {edge_id for edge_id in edges
                        if isinstance(self.mgraph_data.edge(edge_id), edge_type)}

            # Get connected nodes
            for edge_id in edges:
                edge = self.mgraph_data.edge(edge_id)                               # todo: double check this logic
                if edge.from_node_id == node_id:
                    connected_nodes.add(edge.to_node_id())
                else:
                    connected_nodes.add(edge.from_node_id())

        edges = self.get_connecting_edges(connected_nodes)

        self.create_view(nodes_ids = connected_nodes,
                        edges_ids = edges,
                        operation = 'traverse',
                        params    = {'edge_type': edge_type.__name__ if edge_type else None})
        return self


    def filter(self, predicate: Callable[[Domain__MGraph__Node], bool]) -> 'MGraph__Query': # Filters nodes using provided predicate function
        current_nodes, _ = self.get_current_ids()
        filtered_nodes = {
            node_id for node_id in current_nodes
            if predicate(self.mgraph_data.node(node_id))
        }

        filtered_edges = self.get_connecting_edges(filtered_nodes)

        self.create_view(nodes_ids = filtered_nodes,
                        edges_ids = filtered_edges,
                        operation = 'filter',
                        params    = {'predicate': str(predicate)})
        return self

    def print_stats(self):
        pprint(self.stats())

    def stats(self) -> Dict[str, Any]:
        source_nodes, source_edges   = self.get_source_ids()
        current_view                 = self.query_views.current_view()

        stats = { 'source_graph': { 'nodes': len(source_nodes),
                                    'edges': len(source_edges)},
                  'current_view' : current_view.stats()}
        return stats

    def edges_ids(self):
        current_view = self.query_views.current_view()
        return current_view.edges_ids()

    def nodes_ids(self):
        current_view = self.query_views.current_view()
        return current_view.nodes_ids()
