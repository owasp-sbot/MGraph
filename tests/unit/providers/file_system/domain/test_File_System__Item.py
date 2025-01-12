from unittest                                                          import TestCase
from mgraph_ai.providers.file_system.models.Model__File_System__Graph  import Model__File_System__Graph
from mgraph_ai.providers.file_system.models.Model__File_System__Item   import Model__File_System__Item
from mgraph_ai.providers.file_system.schemas.Schema__File_System__Item import Schema__File_System__Item
from mgraph_ai.providers.file_system.domain.File_System__Item          import File_System__Item


class test_File_System__Item(TestCase):

    def setUp(self):                                                                                   # Initialize test data
        self.graph_model = Model__File_System__Graph()
        self.item        = Schema__File_System__Item(folder_name = "test_folder"                           )
        self.item_model  = Model__File_System__Item (data        = self.item                               )
        self.domain_item = File_System__Item        (item        = self.item_model , graph=self.graph_model)

    def test_init(self):                                                                              # Tests basic initialization
        assert type(self.domain_item)              is File_System__Item
        assert type(self.domain_item.folder_name)  is str
        assert self.domain_item.folder_name        == "test_folder"
        assert self.domain_item.created_at         is not None
        assert self.domain_item.modified_at        is not None

    def test__bug__path_calculation(self):                                                                  # Tests path calculation
        # Create a path: root -> folder1 -> folder2 -> test_folder
        root    = self.graph_model.new_node(folder_name="/")
        folder1 = self.graph_model.new_node(folder_name="folder1")
        folder2 = self.graph_model.new_node(folder_name="folder2")

        # self.folder_item = Folder__Node(item= self.domain_item, graph=self.graph_model)  # BUG this is not working
        #self.graph_model.add_node(self.domain_item)                                       # BUG this is also not working

        self.graph_model.new_edge(from_node_id=root   .node_id(), to_node_id=folder1.node_id  ())
        self.graph_model.new_edge(from_node_id=folder1.node_id(), to_node_id=folder2.node_id  ())
        #self.graph_model.new_edge(from_node_id=folder2.node_id(), to_node_id=self.item.node_id())

        path = self.domain_item.path()
        #assert path == ["/", "folder1", "folder2", "test_folder"]
        assert path == []                                                                   # BUG: wrong path
