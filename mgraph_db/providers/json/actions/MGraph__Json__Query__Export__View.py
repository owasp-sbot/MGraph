from mgraph_db.mgraph.domain.Domain__MGraph__Graph                      import Domain__MGraph__Graph
from mgraph_db.providers.json.actions.MGraph__Json__Edit                import MGraph__Json__Edit
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Graph__Data import Schema__MGraph__Json__Graph__Data
from mgraph_db.query.actions.MGraph__Query__Export__View                import MGraph__Query__Export__View


class MGraph__Json__Query__Export__View(MGraph__Query__Export__View):

    def export(self) -> Domain__MGraph__Graph:
        new_graph = super().export()                                                    # Create base graph using parent class
        json_edit = MGraph__Json__Edit(graph=new_graph)                                 # Set up JSON-specific components
        if self.mgraph_query.root_nodes:                                                # if we have root_nodes to map
            graph_data = Schema__MGraph__Json__Graph__Data()                            # reset graph_data
            new_graph.model.data.graph_data = graph_data                                # which includes the root_id value
            with json_edit as _:
                root_property_node = _.add_root_property_node()                         # Add root node  and root property node
                for root_id in self.mgraph_query.root_nodes:                            # Link root nodes to the root property
                    _.new_edge(from_node_id=root_property_node.node_id,
                                to_node_id=root_id)
                # root_node_id = _.data().root_node_id()
                # for node_id in self.mgraph_query.root_nodes:                            # Link root nodes to the root property
                #     _.new_edge(from_node_id=root_node_id,
                #                 to_node_id=node_id)
        return new_graph