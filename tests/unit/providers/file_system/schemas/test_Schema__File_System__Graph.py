from unittest                                                                   import TestCase
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge                              import Schema__MGraph__Edge
from osbot_utils.helpers.Random_Guid                                            import Random_Guid
from osbot_utils.helpers.Timestamp_Now                                          import Timestamp_Now
from mgraph_ai.providers.file_system.schemas.Schema__File_System__Graph         import Schema__File_System__Graph
from mgraph_ai.providers.file_system.schemas.Schema__Folder__Node               import Schema__Folder__Node
from mgraph_ai.providers.file_system.schemas.Schema__File_System__Graph__Config import Schema__File_System__Graph__Config


class test_Schema__File_System__Graph(TestCase):

    def setUp(self):                                                                             # Initialize test data
        self.graph_config = Schema__File_System__Graph__Config(graph_id            = Random_Guid(),
                                                               allow_circular_refs = False        )

        self.fs_graph    = Schema__File_System__Graph(nodes         = {}                          ,
                                                      edges         = {}                          ,
                                                      graph_config  = self.graph_config           ,
                                                      graph_type    = Schema__File_System__Graph)

    def test_init(self):                                                                        # Tests basic initialization and type checking
        assert type(self.fs_graph)              is Schema__File_System__Graph
        assert type(self.fs_graph.graph_config) is Schema__File_System__Graph__Config
        assert self.fs_graph.graph_config       == self.graph_config
        assert len(self.fs_graph.nodes)         == 0
        assert len(self.fs_graph.edges)         == 0

    def test_type_safety_validation(self):                                                      # Tests type safety validations
        with self.assertRaises(ValueError) as context:
            Schema__File_System__Graph(nodes         = "not-a-dict",                                                   # Should be Dict
                                       edges         = {},
                                       graph_config  = self.graph_config,
                                       graph_type    = Schema__File_System__Graph)
        assert 'Invalid type for attribute' in str(context.exception)

    def test_add_folder(self):                                                                  # Tests adding a folder node
        folder_node = Schema__Folder__Node(folder_name = "test_folder",
                                           created_at  = Timestamp_Now()     ,
                                           modified_at = Timestamp_Now()     ,
                                           node_type   = Schema__Folder__Node)

        # Add folder to graph
        self.fs_graph.nodes[Random_Guid()] = folder_node
        assert len(self.fs_graph.nodes) == 1
        assert isinstance(list(self.fs_graph.nodes.values())[0], Schema__Folder__Node)

    def test_folder_structure(self):                                                            # Tests creating a folder structure
        # Create root folder
        root_folder = Schema__Folder__Node(folder_name = "/",
                                           created_at  = Timestamp_Now()     ,
                                           modified_at = Timestamp_Now()     ,
                                           node_type   = Schema__Folder__Node)
        root_id = Random_Guid()
        self.fs_graph.nodes[root_id] = root_folder

        # Create child folder
        child_folder = Schema__Folder__Node(folder_name = "docs"                ,
                                            created_at  = Timestamp_Now()       ,
                                            modified_at = Timestamp_Now()       ,
                                            node_type   = Schema__Folder__Node  )
        child_id = Random_Guid()
        self.fs_graph.nodes[child_id] = child_folder
        edge_id                       = Random_Guid()                                           # Add edge between folders

        self.fs_graph.edges[edge_id] = Schema__MGraph__Edge.from_json( {"from_node_id": root_id,
                                                                        "to_node_id"  : child_id })

        assert len(self.fs_graph.nodes) == 2
        assert len(self.fs_graph.edges) == 1