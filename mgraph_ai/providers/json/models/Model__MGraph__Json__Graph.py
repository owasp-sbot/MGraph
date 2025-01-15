from mgraph_ai.providers.json.models.Model__MGraph__Json__Node              import Model__MGraph__Json__Node
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node__List        import Model__MGraph__Json__Node__List
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node__Property    import Model__MGraph__Json__Node__Property
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node__Value       import Model__MGraph__Json__Node__Value
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node            import Schema__MGraph__Json__Node
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__List      import Schema__MGraph__Json__Node__List
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__Property  import Schema__MGraph__Json__Node__Property
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__Value     import Schema__MGraph__Json__Node__Value
from mgraph_ai.mgraph.models.Model__MGraph__Graph                           import Model__MGraph__Graph
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node__Dict        import Model__MGraph__Json__Node__Dict
from mgraph_ai.providers.json.models.Model__MGraph__Json__Types             import Model__MGraph__Json__Types
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Graph           import Schema__MGraph__Json__Graph
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__Dict      import Schema__MGraph__Json__Node__Dict

class Model__MGraph__Json__Graph(Model__MGraph__Graph):
    data       : Schema__MGraph__Json__Graph
    model_types: Model__MGraph__Json__Types

    def node(self, node_id):
        node  = self.data.nodes.get(node_id)
        if node:
            if node.node_type is Schema__MGraph__Json__Node:            # todo: add a type resolver so that we don't have to hard code all these mappings here
                return Model__MGraph__Json__Node(data=node)
            elif node.node_type is Schema__MGraph__Json__Node__Dict:
                return Model__MGraph__Json__Node__Dict(data=node)
            elif node.node_type is Schema__MGraph__Json__Node__List:
                return Model__MGraph__Json__Node__List(data=node)
            elif node.node_type is Schema__MGraph__Json__Node__Value:
                return Model__MGraph__Json__Node__Value(data=node)
            elif node.node_type is Schema__MGraph__Json__Node__Property:
                return Model__MGraph__Json__Node__Property(data=node)