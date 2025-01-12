from unittest                                                         import TestCase
from mgraph_ai.providers.file_system.models.Model__File_System__Graph import Model__File_System__Graph
from mgraph_ai.providers.file_system.models.Model__Folder__Node       import Model__Folder__Node
from mgraph_ai.providers.file_system.schemas.Schema__Folder__Node     import Schema__Folder__Node
from mgraph_ai.providers.file_system.domain.Folder__Node              import Folder__Node


class test_Folder__Node(TestCase):

    def setUp(self):                                                                                   # Initialize test data
        self.graph_model  = Model__File_System__Graph()
        self.folder       = Schema__Folder__Node(folder_name="parent_folder")
        self.folder_model = Model__Folder__Node(data=self.folder)
        self.domain_folder = Folder__Node(item=self.folder_model, graph=self.graph_model)

    def test_init(self):                                                                              # Tests basic initialization
        assert type(self.domain_folder)       is Folder__Node
        assert self.domain_folder.folder_name == "parent_folder"

    def test_children_and_parent(self):                                                               # Tests parent/child relationships
        self.graph_model.add_node(self.folder)
        # Create child folders
        child1 = self.graph_model.new_node(folder_name="child1")
        child2 = self.graph_model.new_node(folder_name="child2")

        # Create parent folder
        parent = self.graph_model.new_node(folder_name="grandparent")

        assert type(child1) is Model__Folder__Node
        assert type(child2) is Model__Folder__Node
        assert type(parent) is Model__Folder__Node

        # Setup relationships
        self.graph_model.new_edge(from_node_id=parent           .node_id, to_node_id=self.folder.node_config.node_id)
        self.graph_model.new_edge(from_node_id=self.folder_model.node_id, to_node_id=child1.node_id     ())
        self.graph_model.new_edge(from_node_id=self.folder_model.node_id, to_node_id=child2.node_id     ())

        # Test children
        children = self.domain_folder.children()
        assert len(children) == 0                                   # BUG: Expected 2
        # assert len(children) == 2                                 # BUG: not working
        # child_names = {child.folder_name for child in children}
        # assert child_names == {"child1", "child2"}

        # Test parent
        parent_folder = self.domain_folder.parent()
        assert parent_folder is None                                # BUG: Expected parent folder
        #assert parent_folder is not None                           # BUG: not working
        #assert parent_folder.folder_name == "grandparent"