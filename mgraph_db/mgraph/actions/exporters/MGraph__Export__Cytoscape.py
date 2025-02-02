from typing                                                     import Dict, Any
from mgraph_db.mgraph.actions.exporters.MGraph__Export__Base    import MGraph__Export__Base
from mgraph_db.mgraph.actions.exporters.Model__Cytoscape__Types import Model__Cytoscape__Node, Model__Cytoscape__Edge
from mgraph_db.mgraph.actions.exporters.Model__Cytoscape__Types import Model__Cytoscape__Node__Data, Model__Cytoscape__Edge__Data
from mgraph_db.mgraph.actions.exporters.Model__Cytoscape__Types import Model__Cytoscape__Elements

class MGraph__Export__Cytoscape(MGraph__Export__Base):

    def create_node_data(self, node) -> Dict[str, Any]:                                             # Create Cytoscape-specific node data
        node_data = Model__Cytoscape__Node__Data(id    = str(node.node_id)                ,         # Create strongly typed node data
                                                 type  = node.node.data.node_type.__name__,
                                                 label = self.get_node_label(node)        )


        return Model__Cytoscape__Node(data  = node_data).json()                                          # Return complete node structure

    def create_edge_data(self, edge) -> Dict[str, Any]:                                             # Create Cytoscape-specific edge data
        edge_data = Model__Cytoscape__Edge__Data( id     = str(edge.edge_id      )          ,       # Create strongly typed edge data
                                                  source = str(edge.from_node_id())         ,
                                                  target = str(edge.to_node_id  ())         ,
                                                  type   = edge.edge.data.edge_type.__name__)

        # Return complete edge structure
        return Model__Cytoscape__Edge(data  = edge_data).json()

    def format_output(self) -> Dict[str, Any]:                                              # Format data specifically for Cytoscape.js
        elements = Model__Cytoscape__Elements(nodes = list(self.context.nodes.values()),    # Create strongly typed elements structure
                                              edges = list(self.context.edges.values()))
        return {'elements': elements.json()}                                                # Return in Cytoscape's expected format

    def get_node_label(self, node) -> str:                                                  # Helper to get node label
        for attr in ('label', 'name', 'value'):                                             # check if these values exist
            node_label = getattr(node.node_data, attr, None)                                # get the value
            if node_label:                                                                  # if it not empty
                return str(node_label)                                                      # return it

        return node.node.data.node_type.__name__