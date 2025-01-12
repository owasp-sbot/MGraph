from mgraph_ai.mgraph.models.Model__MGraph__Graph       import Model__MGraph__Graph
from mgraph_ai.mgraph.models.Model__MGraph__Node        import Model__MGraph__Node
from osbot_utils.type_safe.Type_Safe                    import Type_Safe
from osbot_utils.type_safe.methods.type_safe_property import set_as_property

class Domain__MGraph__Node(Type_Safe):                                                      # Domain class for nodes
    node : Model__MGraph__Node                                                              # Reference to node model
    graph: Model__MGraph__Graph                                                             # Reference to graph model

    node_data = set_as_property('node.data'               , 'node_data')                    # Node configuration property
    node_id   = set_as_property('node.data.node_data'     , 'node_id'  )                    # Node ID property
    graph_id  = set_as_property ('graph.data.graph_config', 'graph_id' )                    # Graph ID property

