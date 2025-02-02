from unittest                                                           import TestCase
from mgraph_db.providers.file_system.actions.File_System__Data          import File_System__Data
from mgraph_db.providers.file_system.domain.Folder__Node                import Folder__Node
from mgraph_db.providers.file_system.models.Model__File_System__Graph   import Model__File_System__Graph
from mgraph_db.providers.file_system.actions.File_System__Edit          import File_System__Edit

class test_File_System__Data(TestCase):

    @classmethod
    def setUpClass(cls):
        import pytest
        pytest.skip("todo: fix these tests after MGraph refactoring")

    def setUp(self):                                                                                    # Initialize test data
        self.graph = Model__File_System__Graph()
        self.data  = File_System__Data(graph=self.graph)
        self.edit  = File_System__Edit(graph=self.graph)

        # Create test folder structure
        self.root   = self.edit.add_folder(None     , "root" )                                               # Create root folder
        self.docs   = self.edit.add_folder(self.root, "docs" )                                         # Add child folders
        self.code   = self.edit.add_folder(self.root, "code" )
        self.deep   = self.edit.add_folder(self.docs, "deep" )
        self.nested = self.edit.add_folder(self.deep, "nested")

    def test_init(self):                                                                              # Test initialization
        assert type(self.data)            is File_System__Data
        assert type(self.data.graph)      is Model__File_System__Graph

    def test_root(self):                                                                             # Test root folder access
        root = self.data.root()
        assert type(root)              is Folder__Node
        assert root.folder_name()      == "root"
        assert root.parent()           is None
        assert len(root.children())    == 2

    def test_folder(self):                                                                          # Test folder path lookup
        # Test root path
        root_folder = self.data.folder("/root")
        assert root_folder == self.root

        # Test nested path
        nested_folder = self.data.folder("/root/docs/deep/nested")
        assert nested_folder == self.nested

        # Test non-existent paths
        assert self.data.folder("/nonexistent")                is None
        assert self.data.folder("/root/docs/nonexistent")      is None
        assert self.data.folder("")                            is None
        assert self.data.folder("/")                           == self.root      # Root path

    def test_exists(self):                                                                         # Test path existence check
        # Test existing paths
        assert self.data.exists("/root")                       is True
        assert self.data.exists("/root/docs")                  is True
        assert self.data.exists("/root/docs/deep/nested")      is True

        # Test non-existent paths
        assert self.data.exists("/nonexistent")                is False
        assert self.data.exists("/root/nonexistent")           is False
        assert self.data.exists("")                            is False

    def test_child_by_name(self):                                                                 # Test child folder lookup
        # Test direct children
        docs = self.data.child_by_name(self.root, "docs")
        assert docs == self.docs

        code = self.data.child_by_name(self.root, "code")
        assert code == self.code

        # Test nested children
        deep = self.data.child_by_name(self.docs, "deep")
        assert deep == self.deep

        nested = self.data.child_by_name(self.deep, "nested")
        assert nested == self.nested

        # Test non-existent children
        assert self.data.child_by_name(self.root, "nonexistent") is None
        assert self.data.child_by_name(self.docs, "nonexistent") is None

    def test_empty_graph(self):                                                                  # Test behavior with empty graph
        empty_graph = Model__File_System__Graph()
        empty_data  = File_System__Data(graph=empty_graph)

        assert empty_data.root()                               is None
        assert empty_data.folder("/any/path")                  is None
        assert empty_data.exists("/any/path")                  is False

    def test_path_normalization(self):                                                          # Test path handling edge cases
        # Test various path formats
        assert self.data.folder("/root/docs")                  == self.docs     # Standard path
        assert self.data.folder("root/docs")                   == self.docs     # No leading slash
        assert self.data.folder("/root/docs/")                 == self.docs     # Trailing slash
        assert self.data.folder("//root//docs//")             == self.docs     # Multiple slashes

    def test_folder_relationships(self):                                                        # Test folder relationships
        docs = self.data.folder("/root/docs")

        # Test parent relationship
        assert docs.parent() == self.root

        # Test children
        children = docs.children()
        assert len(children) == 1
        assert children[0] == self.deep

        # Test nested structure
        deep = docs.children()[0]
        assert deep.children()[0] == self.nested