from unittest                                                            import TestCase
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Default__Types import Schema__Mermaid__Default__Types
from osbot_utils.helpers.Random_Guid                                     import Random_Guid
from osbot_utils.helpers.Safe_Id                                         import Safe_Id
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge           import Schema__Mermaid__Edge
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge__Config   import Schema__Mermaid__Edge__Config
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Graph          import Schema__Mermaid__Graph
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Graph__Config  import Schema__Mermaid__Graph__Config
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node           import Schema__Mermaid__Node
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node__Data   import Schema__Mermaid__Node__Data

class test_Schema__Mermaid__Graph(TestCase):

    def setUp(self):                                                                # Initialize test data
        self.default_types = Schema__Mermaid__Default__Types()
        self.graph_config  = Schema__Mermaid__Graph__Config(graph_id             = Random_Guid()        ,
                                                            allow_circle_edges   = True                 ,
                                                            allow_duplicate_edges= False                ,
                                                            graph_title         = "Test Graph"          )
        self.node          = Schema__Mermaid__Node         (node_data = Schema__Mermaid__Node__Data(node_id=Random_Guid()),
                                                            node_type   = Schema__Mermaid__Node                                   ,
                                                            key         = Safe_Id("node_1")                                       ,
                                                            label       = "Test Node"                                             )
        self.edge          = Schema__Mermaid__Edge         (edge_config  = Schema__Mermaid__Edge__Config(edge_id= Random_Guid()   ),
                                                            edge_type    = Schema__Mermaid__Edge                                   ,
                                                            from_node_id = Random_Guid()                                           ,
                                                            to_node_id   = Random_Guid()                                           ,
                                                            label        = "Test Edge"                                             )
        self.graph          = Schema__Mermaid__Graph       (default_types = self.default_types                       ,
                                                            edges        = {self.edge.edge_config.edge_id: self.edge},
                                                            nodes        = {self.node.node_data.node_id: self.node},
                                                            graph_config = self.graph_config                         ,
                                                            graph_type   = Schema__Mermaid__Graph                    ,
                                                            mermaid_code = ["graph TD", "A --> B"]                   )

    def test_init(self):                                                            # Tests basic initialization and type checking
        assert type(self.graph)          is Schema__Mermaid__Graph
        assert self.graph.graph_config   == self.graph_config
        assert len(self.graph.nodes)     == 1
        assert len(self.graph.edges)     == 1
        assert type(self.graph.mermaid_code) is list
        assert len(self.graph.mermaid_code)  == 2

    def test_type_safety_validation(self):                                          # Tests type safety validations
        with self.assertRaises(ValueError) as context:
            Schema__Mermaid__Graph( edges        = "not-a-dict"          ,
                                    nodes        = {}                    ,
                                    graph_config = self.graph_config     ,
                                    graph_type   = Schema__Mermaid__Graph,
                                    mermaid_code = ["graph TD"]          )
        assert "Invalid type for attribute" in str(context.exception)

        with self.assertRaises(ValueError) as context:
            Schema__Mermaid__Graph( edges        = {}                    ,
                                    nodes        = {}                    ,
                                    graph_config = self.graph_config     ,
                                    graph_type   = Schema__Mermaid__Graph,
                                    mermaid_code = "not-a-list"          )
        assert "Invalid type for attribute" in str(context.exception)


