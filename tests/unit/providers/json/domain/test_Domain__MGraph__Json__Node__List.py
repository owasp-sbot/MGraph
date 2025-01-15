import pytest
from unittest                                                         import TestCase
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node      import Schema__MGraph__Json__Node__List
from osbot_utils.utils.Objects                                        import __, type_full_name
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node       import Domain__MGraph__Json__Node
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node__List import Domain__MGraph__Json__Node__List

class test_Domain__MGraph__Json__Node__List(TestCase):

    @classmethod
    def setUpClass(cls):  # Initialize test data
        pytest.skip("todo: fix test")
        cls.domain_graph     = Domain__MGraph__Json__Node      ()
        cls.domain_node_list = Domain__MGraph__Json__Node__List()

    def test__init__(self):                                                                 # Test basic initialization
        with self.domain_node_list as _:
            assert type(_)                                   is Domain__MGraph__Json__Node__List
            assert isinstance(_, Domain__MGraph__Json__Node) is True
            assert _.obj() == __(node  = __(data=__(node_data  = __()                                             ,
                                                    node_id    = _.node_id                                        ,
                                                    node_type  = type_full_name(Schema__MGraph__Json__Node__List))),
                                 graph = _.graph.obj())

    def test_add_item(self):                                                             # Test adding items
        with self.domain_node_list as _:
            _.add("test_value")
            return
            items = _.items()

            assert len(items) == 1
            assert items[0] == "test_value"

    def test_remove_item(self):                                                          # Test removing items
        self.list_node.add("value1")
        self.list_node.add("value2")
        self.list_node.add("value1")  # Duplicate value

        assert self.list_node.remove("value1") is True
        items = self.list_node.items()
        assert len(items) == 2
        assert items.count("value1") == 1

    def test_clear_items(self):                                                          # Test clearing all items
        self.list_node.add("value1")
        self.list_node.add("value2")
        self.list_node.clear()

        assert len(self.list_node.items()) == 0

    def test_extend_nodes(self):                                                         # Test extending with multiple nodes
        node1 = self.graph.new_node(value="value1", value_type=str)
        node2 = self.graph.new_node(value="value2", value_type=str)

        self.list_node.extend([node1, node2])
        items = self.list_node.items()

        assert len(items) == 2
        assert items == ["value1", "value2"]