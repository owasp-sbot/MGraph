from typing                                                              import Dict, Any, List
from mgraph_ai.providers.mermaid.domain.Mermaid                          import Mermaid
from mgraph_ai.providers.mermaid.domain.Mermaid__Graph                   import Mermaid__Graph
from osbot_utils.helpers.Safe_Id                                         import Safe_Id
from osbot_utils.helpers.Random_Guid                                     import Random_Guid
from mgraph_ai.mgraph.utils.MGraph__Random_Graph                         import MGraph__Random_Graph
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node           import Schema__Mermaid__Node
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge           import Schema__Mermaid__Edge
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Config   import Schema__Mermaid__Node__Config
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge__Config   import Schema__Mermaid__Edge__Config
from mgraph_ai.providers.mermaid.models.Model__Mermaid__Graph            import Model__Mermaid__Graph
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Graph          import Schema__Mermaid__Graph
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Default__Types import Schema__Mermaid__Default__Types
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Graph__Config  import Schema__Mermaid__Graph__Config

class Mermaid__Random_Graph(MGraph__Random_Graph):

    def setup(self) -> 'Mermaid__Random_Graph':                                                                             # Initialize with Mermaid-specific components
        self.graph_config = Schema__Mermaid__Graph__Config(graph_id      = Random_Guid())
        self.graph_data   = Schema__Mermaid__Graph        (default_types = Schema__Mermaid__Default__Types(),
                                                           edges        = {}                                ,
                                                           nodes        = {}                                ,
                                                           graph_config = self.graph_config                 ,
                                                           graph_type   = Schema__Mermaid__Graph            ,
                                                           mermaid_code = []                                )
        self.graph__model = Model__Mermaid__Graph         (data=self.graph_data)

        self.graph__graph = Mermaid__Graph               (model         = self.graph__model                  )
        self.graph        = Mermaid                      (graph         = self.graph__graph                  )
        return self

    def create_mermaid_node(self, key: str, label: str = None, value: Any = None) -> Schema__Mermaid__Node:             # create a Mermaid-specific node with the given parameters."""
        safe_key = Safe_Id(key)
        node_config = Schema__Mermaid__Node__Config(node_id    = Random_Guid(),
                                                    value_type = str          )
        return Schema__Mermaid__Node                (attributes  = {},
                                                     node_config = node_config,
                                                     node_type   = Schema__Mermaid__Node,
                                                     value       = value or f"value_{safe_key}",
                                                     key         = safe_key,
                                                     label       = label or f"Label {safe_key}")

    def create_mermaid_edge(self, from_node: Schema__Mermaid__Node,                                                     # create a Mermaid-specific edge between nodes
                                  to_node  : Schema__Mermaid__Node,
                                  label    : str = None) -> Schema__Mermaid__Edge:

        edge_config = Schema__Mermaid__Edge__Config(edge_id        = Random_Guid()                  )
        return Schema__Mermaid__Edge               (attributes     = {}                             ,
                                                    edge_config    = edge_config                    ,
                                                    edge_type      = Schema__Mermaid__Edge          ,
                                                    from_node_id   = from_node.node_config.node_id  ,
                                                    to_node_id     = to_node.node_config.node_id    ,
                                                    label          = label or f"Edge {from_node.key} to {to_node.key}")

    def create_nodes(self, num_nodes: int) -> List[Schema__Mermaid__Node]:                                             # Create specified number of Mermaid nodes
        if num_nodes < 0:
            raise ValueError("Number of nodes cannot be negative")

        nodes = []
        for i in range(num_nodes):
            node = self.create_mermaid_node(key=f'key_{i}')
            self.graph__model.add_node(node)
            nodes.append(node)
        return nodes

    def create_random_edges(self, nodes: List[Schema__Mermaid__Node], num_edges: int) -> None:                         # Create random edges between Mermaid nodes
        if not nodes:
            raise ValueError("No nodes available to create edges")
        if num_edges < 0:
            raise ValueError("Number of edges cannot be negative")

        from osbot_utils.utils.Misc import random_int
        num_nodes = len(nodes)

        for _ in range(num_edges):
            from_idx = random_int(max=num_nodes) - 1
            to_idx   = random_int(max=num_nodes) - 1

            edge = self.create_mermaid_edge(from_node = nodes[from_idx],
                                           to_node   = nodes[to_idx  ])
            self.graph__model.add_edge(edge)

    def create_test_graph(self, num_nodes: int = 3, num_edges: int = None) -> Mermaid:                     # Create a test graph with nodes and edges
        if not self.graph__model:
            self.setup()

        nodes = self.create_nodes(num_nodes)

        if num_edges is None:
            num_edges = num_nodes * 2                                                                                    # Default to twice as many edges as nodes

        self.create_random_edges(nodes, num_edges)
        return self.graph

# Static helper functions
def create_test_mermaid_graph(num_nodes: int = 2, num_edges: int = 2) -> Mermaid:                                    # Create a test Mermaid graph with the specified number of nodes and edges
    return Mermaid__Random_Graph().create_test_graph(num_nodes=num_nodes, num_edges=num_edges)

def create_empty_mermaid_graph() -> Mermaid:                                                                            # Create an empty Mermaid graph
    return Mermaid__Random_Graph().setup().graph