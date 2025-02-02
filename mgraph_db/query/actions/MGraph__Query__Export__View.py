from mgraph_db.query.MGraph__Query                                  import MGraph__Query
from mgraph_db.mgraph.domain.Domain__MGraph__Graph                  import Domain__MGraph__Graph
from mgraph_db.query.models.Model__MGraph__Query__Export__View      import Model__MGraph__Query__Export__View
from mgraph_db.query.schemas.Schema__MGraph__Query__Export__View    import Schema__MGraph__Query__Export__View
from osbot_utils.type_safe.Type_Safe                                import Type_Safe


class MGraph__Query__Export__View(Type_Safe):
    mgraph_query : MGraph__Query

    def export(self) -> Domain__MGraph__Graph:                      # Creates a new graph from a view's IDs

        return self.create_graph()                                                                            # Create and return new graph

    def create_graph(self) -> Domain__MGraph__Graph:                                                                    # Creates a new independent graph from the view"""

        with self.mgraph_query as _:
            graph_domain  = _.mgraph_data.graph
            graph_model   = graph_domain.model
            graph_schema  = graph_model.data
            target_view   = _.current_view()
            nodes_ids     = target_view.nodes_ids()
            edges_ids     = target_view.edges_ids()

        schema = Schema__MGraph__Query__Export__View(source_graph = graph_schema,                                    # Create export view schema
                                                     nodes_ids    = nodes_ids   ,
                                                     edges_ids    = edges_ids   )
        model              = Model__MGraph__Query__Export__View(data=schema)  # Create model and domain layers
        type__graph        = type(graph_domain             )
        type__model        = type(graph_model              )
        type__model_types  = type(graph_model.model_types  )
        type__domain_types = type(graph_domain.domain_types)

        new_graph    = model.create_new_graph()                                                                       # Create new graph at schema layer using Type_Safe serialization
        model.clone_nodes(new_graph)                                                                               # Clone nodes and edges using Type_Safe serialization
        model.clone_edges(new_graph)

        model_types = type__model_types.from_json(graph_model.model_types.json())                   # Create model layer using Type_Safe serialization

        model = type__model(data        = new_graph,
                            model_types = model_types)

        domain_types = type__domain_types.from_json(graph_domain.domain_types.json())               # Create domain layer using Type_Safe serialization

        return type__graph(model        = model,
                           domain_types = domain_types)