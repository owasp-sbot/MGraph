from mgraph_ai.mgraph.models.Model__MGraph__Graph                     import Model__MGraph__Graph
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node__Dict  import Model__MGraph__Json__Node__Dict
from mgraph_ai.providers.json.models.Model__MGraph__Json__Types       import Model__MGraph__Json__Types
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Graph      import Schema__MGraph__Json__Graph
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__Dict import Schema__MGraph__Json__Node__Dict


class Model__MGraph__Json__Graph(Model__MGraph__Graph):
    data       : Schema__MGraph__Json__Graph
    model_types: Model__MGraph__Json__Types

    def add_node__dict(self):
        data = Schema__MGraph__Json__Node__Dict()
        node = Model__MGraph__Json__Node__Dict(data=data)
        self.data.nodes[node.node_id] = data  # for now, we need to add this directly here
        # self.add_node(data)                                        # todo: improve add_node to receive the model to create since at the not going ot create a Model__MGraph__Json__Node__Dict

        return node