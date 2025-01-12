from unittest                                                         import TestCase
from mgraph_ai.mgraph.models.Model__MGraph__Node                      import Model__MGraph__Node
from osbot_utils.type_safe.Type_Safe                                  import Type_Safe
from osbot_utils.utils.Objects                                        import base_types
from mgraph_ai.providers.file_system.models.Model__File_System__Graph import Model__File_System__Graph
from mgraph_ai.providers.file_system.models.Model__File_System__Item  import Model__File_System__Item
from mgraph_ai.providers.file_system.models.Model__Folder__Node       import Model__Folder__Node
from mgraph_ai.providers.file_system.domain.File_System__Graph        import File_System__Graph
from mgraph_ai.providers.file_system.domain.Folder__Node              import Folder__Node


class test_File_System__Graph(TestCase):

    def setUp(self):                                                                    # Initialize test data
        self.graph_model = Model__File_System__Graph()
        self.domain_graph = File_System__Graph(model=self.graph_model)

    def test_init(self):                                                                # Tests basic initialization
        assert type(self.domain_graph) is File_System__Graph
        assert self.domain_graph.allow_circular_refs() is False

    def test__bug__root_folder_detection(self):  # Tests root folder operations
        # Create root and some child folders
        root = self.graph_model.new_node(folder_name="/")
        folder1 = self.graph_model.new_node(folder_name="folder1")
        folder2 = self.graph_model.new_node(folder_name="folder2")

        self.graph_model.new_edge(from_node_id=root.node_id(), to_node_id=folder1.node_id())
        self.graph_model.new_edge(from_node_id=root.node_id(), to_node_id=folder2.node_id())

        # Test root detection
        root_folder = self.domain_graph.root_folder()
        assert root_folder is not None
        assert root_folder.folder_name == "/"

        # Verify root has no parent
        assert root_folder.parent() is None

        # Verify root has correct children
        children = root_folder.children()
        assert len(children) == 0                                       # BUG
        # assert len(children) == 2                                       # BUG
        # child_names = {child.folder_name for child in children}       # BUG
        # assert child_names == {"folder1", "folder2"}                    # BUG

    def test__bug__complex_structure(self):  # Tests complex folder structure
        # Create a more complex structure:
        # /
        # ├── folder1
        # │   ├── subfolder1
        # │   └── subfolder2
        # └── folder2
        #     └── subfolder3

        root       = self.graph_model.new_node(folder_name="/"         )
        folder1    = self.graph_model.new_node(folder_name="folder1"   )
        folder2    = self.graph_model.new_node(folder_name="folder2"   )
        subfolder1 = self.graph_model.new_node(folder_name="subfolder1")
        subfolder2 = self.graph_model.new_node(folder_name="subfolder2")
        subfolder3 = self.graph_model.new_node(folder_name="subfolder3")

        assert type      (root   ) is Model__Folder__Node
        assert type      (folder1) is Model__Folder__Node
        assert base_types(root   ) == [Model__File_System__Item, Model__MGraph__Node, Type_Safe, object]
        assert base_types(folder1) == base_types(root)

        # Create structure
        self.graph_model.new_edge(from_node_id=root.node_id()   , to_node_id=folder1.node_id())
        self.graph_model.new_edge(from_node_id=root.node_id()   , to_node_id=folder2.node_id())
        self.graph_model.new_edge(from_node_id=folder1.node_id(), to_node_id=subfolder1.node_id())
        self.graph_model.new_edge(from_node_id=folder1.node_id(), to_node_id=subfolder2.node_id())
        self.graph_model.new_edge(from_node_id=folder2.node_id(), to_node_id=subfolder3.node_id())


        # Test paths
        root_folder    = self.domain_graph.root_folder()
        folder1_obj    = Folder__Node(item=folder1    , graph=self.graph_model)
        subfolder1_obj = Folder__Node(item=subfolder1 , graph=self.graph_model)

        assert root_folder.path()    == ["/"]
        #assert folder1_obj.path()    == ["/", "folder1"]                           # BUG
        assert folder1_obj.path() == ["folder1"]                                    # BUG: should be ["/", "folder1"]
        #assert subfolder1_obj.path() == ["/", "folder1", "subfolder1"]             # BUG
        assert subfolder1_obj.path() == ["subfolder1"]                              # BUG: should be ["/", "folder1", "subfolder1"]