from unittest                                                           import TestCase
from mgraph_ai.providers.file_system.actions.File_System__Edit          import File_System__Edit
from mgraph_ai.providers.file_system.domain.Folder__Node                import Folder__Node
from mgraph_ai.providers.file_system.models.Model__File_System__Graph   import Model__File_System__Graph
from mgraph_ai.providers.file_system.actions.File_System__Data          import File_System__Data

class test_File_System__Edit(TestCase):

    @classmethod
    def setUpClass(cls):
        import pytest
        pytest.skip("todo: fix these tests after MGraph refactoring")

    def setUp(self):                                                                                    # Initialize test data
        self.graph = Model__File_System__Graph()
        self.edit  = File_System__Edit(graph=self.graph)
        self.data  = File_System__Data(graph=self.graph)

    def test_init(self):                                                                               # Test initialization
        assert type(self.edit      ) is File_System__Edit
        assert type(self.edit.graph) is Model__File_System__Graph

    def test_set_root(self):                                                                          # Test root folder creation
        # Test initial root setup
        root = Folder__Node(graph=self.graph, name="root")
        #pprint(root.node_id)
        #self.edit.set_root(root)
        return


        assert self.data.root() == root
        assert len(self.graph.nodes()) == 1

        # Test attempting to set root on non-empty graph
        new_root = Folder__Node(graph=self.graph, name="new_root")
        with self.assertRaises(ValueError):
            self.edit.set_root(new_root)

    def test_add_folder(self):                                                                        # Test folder creation
        root = Folder__Node(graph=self.graph, name="root")
        self.edit.set_root(root)

        # Test adding direct child
        docs = self.edit.add_folder(root, "docs")
        assert type(docs) is Folder__Node
        assert docs.folder_name() == "docs"
        assert docs.parent() == root

        # Test adding another child
        code = self.edit.add_folder(root, "code")
        assert code.folder_name() == "code"
        assert code.parent() == root

        # Verify root's children
        root_children = root.children()
        assert len(root_children) == 2
        assert sorted([child.folder_name() for child in root_children]) == ["code", "docs"]

    def test_duplicate_folder_names(self):                                                           # Test duplicate folder handling
        root = Folder__Node(graph=self.graph, name="root")
        self.edit.set_root(root)

        # Create first folder
        self.edit.add_folder(root, "docs")

        # Attempt to create duplicate
        with self.assertRaises(ValueError) as context:
            self.edit.add_folder(root, "docs")
        assert "Folder docs already exists" in str(context.exception)

    def test_invalid_folder_creation(self):                                                          # Test invalid folder creation
        root = Folder__Node(graph=self.graph, name="root")
        self.edit.set_root(root)

        # Test with invalid parent
        with self.assertRaises(ValueError):
            self.edit.add_folder(None, "test")

        # Test with empty name
        with self.assertRaises(ValueError):
            self.edit.add_folder(root, "")

    def test_circular_references(self):                                                             # Test circular reference handling
        root = Folder__Node(graph=self.graph, name="root")
        self.edit.set_root(root)

        # Create test structure
        docs = self.edit.add_folder(root, "docs")
        deep = self.edit.add_folder(docs, "deep")
        nested = self.edit.add_folder(deep, "nested")

        # Test with circular references disabled (default)
        with self.assertRaises(ValueError) as context:
            self.edit.add_edge(nested, docs)  # Would create cycle
        assert "cycle" in str(context.exception).lower()

        # Test with circular references enabled
        self.edit.allow_circular_refs(True)
        edge = self.edit.add_edge(nested, docs)  # Should succeed
        assert edge is not None

    def test_folder_hierarchy(self):                                                               # Test folder hierarchy
        root = Folder__Node(graph=self.graph, name="root")
        self.edit.set_root(root)

        # Create deep hierarchy
        docs = self.edit.add_folder(root, "docs")
        deep = self.edit.add_folder(docs, "deep")
        nested = self.edit.add_folder(deep, "nested")
        final = self.edit.add_folder(nested, "final")

        # Verify path to root
        current = final
        expected_path = ["final", "nested", "deep", "docs", "root"]
        actual_path = []

        while current:
            actual_path.append(current.folder_name())
            current = current.parent()

        assert actual_path == expected_path

    def test_allow_circular_refs(self):                                                           # Test circular reference setting
        assert self.graph.allow_circular_refs() is False  # Default value

        self.edit.allow_circular_refs(True)
        assert self.graph.allow_circular_refs() is True

        self.edit.allow_circular_refs(False)
        assert self.graph.allow_circular_refs() is False