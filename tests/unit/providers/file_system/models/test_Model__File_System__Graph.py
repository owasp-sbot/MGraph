from unittest                                                         import TestCase
from mgraph_ai.mgraph.models.Model__MGraph__Edge                      import Model__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge                    import Schema__MGraph__Edge
from mgraph_ai.providers.file_system.models.Model__File_System__Graph import Model__File_System__Graph
from mgraph_ai.providers.file_system.models.Model__Folder__Node       import Model__Folder__Node
from mgraph_ai.providers.file_system.schemas.Schema__Folder__Node     import Schema__Folder__Node


class test_Model__File_System__Graph(TestCase):

    def setUp(self):                                                                                   # Initialize test data
        self.model = Model__File_System__Graph()

    def test_init(self):                                                                              # Tests basic initialization
        assert type(self.model)                 is Model__File_System__Graph
        assert self.model.allow_circular_refs() is False

    def test_new_edge(self):
        with self.model as _:
            node_1_id = _.new_node().node_id
            node_2_id = _.new_node().node_id
            edge      = _.new_edge(from_node_id=node_1_id, to_node_id=node_2_id)

            assert _.model_types.edge_model_type  is Model__MGraph__Edge
            assert _.data.schema_types.edge_type  is Schema__MGraph__Edge
            assert type(edge)                     is Model__MGraph__Edge

    def test_new_node(self):
        with self.model as _:
            assert type(_)                         is Model__File_System__Graph
            assert _.model_types.node_model_type is Model__Folder__Node
            assert _.data.schema_types.node_type   is Schema__Folder__Node
            node = _.new_node()
            assert type(node)                      is Model__Folder__Node

    def test__bug__cycle_detection__is_not_working(self):                                                                   # Tests cycle detection
        # Create nodes
        node1 = self.model.new_node(folder_name="folder1")
        node2 = self.model.new_node(folder_name="folder2")
        node3 = self.model.new_node(folder_name="folder3")

        # Test valid tree structure
        self.model.new_edge(from_node_id=node1.node_id, to_node_id=node2.node_id)
        self.model.new_edge(from_node_id=node2.node_id, to_node_id=node3.node_id)

        assert self.model.validate_no_cycles(node1.node_id, node3.node_id) is True

        # Test cycle detection
        # with self.assertRaises(ValueError) as context:
        #     self.model.new_edge(from_node_id=node3.node_id, to_node_id=node1.node_id)      # BUG: this is not being detected
        #     self.model.new_edge(from_node_id=node1.node_id, to_node_id=node3.node_id)      # BUG: we should also pick up this one this is correctly pickup by accident
        # assert "create a cycle" in str(context.exception)


        # Test with circular refs allowed
        self.model.set_allow_circular_refs(True)

        assert len(self.model.edges()) == 2
        self.model.new_edge(from_node_id=node3.node_id, to_node_id=node1.node_id)               # Should work, but not because the check is in place
        assert len(self.model.edges()) == 3

