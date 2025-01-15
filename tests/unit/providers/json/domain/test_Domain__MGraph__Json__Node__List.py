import pytest
from unittest                                                           import TestCase
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Graph        import Domain__MGraph__Json__Graph
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__List  import Schema__MGraph__Json__Node__List
from osbot_utils.utils.Objects                                          import __, type_full_name
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node         import Domain__MGraph__Json__Node
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node__List   import Domain__MGraph__Json__Node__List

class test_Domain__MGraph__Json__Node__List(TestCase):

    @classmethod
    def setUpClass(cls):
        pytest.skip("todo: fix tests")

    def setUp(self):                                                      # Initialize test data
        self.domain_graph = Domain__MGraph__Json__Graph()
        self.domain_node_list = Domain__MGraph__Json__Node__List()

    def test__init__(self):                                              # Test basic initialization
        with self.domain_node_list as _:
            assert type(_) is Domain__MGraph__Json__Node__List
            assert isinstance(_, Domain__MGraph__Json__Node) is True
            assert _.obj() == __(node=__(data=__(node_data=__(),
                                               node_id=_.node_id,
                                               node_type=type_full_name(Schema__MGraph__Json__Node__List))),
                               graph=_.graph.obj())

    def test_add_primitive_values(self):                                 # Test adding primitive values
        with self.domain_node_list as _:
            assert _.graph.nodes_ids() == []
            assert _.graph.edges_ids() == []
            _.add("test_string")
            #pprint(_.graph.json())
            return
            _.add(42)
            _.add(True)
            _.add(None)
            
            items = _.items()
            assert len(items) == 4
            assert items == ["test_string", 42, True, None]

    def test_add_dict(self):                                            # Test adding dictionary
        with self.domain_node_list as _:
            test_dict = {"key1": "value1", "key2": 42}
            _.add(test_dict)
            
            items = _.items()
            assert len(items) == 1
            assert items[0] == test_dict

    def test_add_nested_list(self):                                     # Test adding nested list
        with self.domain_node_list as _:
            test_list = [1, 2, ["a", "b"]]
            _.add(test_list)
            
            items = _.items()
            assert len(items) == 1
            assert items[0] == [1, 2, ["a", "b"]]

    def test_complex_structure(self):                                   # Test complex nested structure
        with self.domain_node_list as _:
            complex_data = [
                "string",
                {"key": "value"},
                [1, 2, 3],
                {"nested": {"a": 1, "b": [True, False]}}
            ]
            
            for item in complex_data:
                _.add(item)
            
            items = _.items()
            assert len(items) == 4
            assert items == complex_data

    def test_clear(self):                                              # Test clearing all items
        with self.domain_node_list as _:
            _.add("value1")
            _.add({"key": "value"})
            _.add([1, 2, 3])
            
            assert len(_.items()) == 3
            _.clear()
            assert len(_.items()) == 0

    def test_extend(self):                                             # Test extending with multiple items
        with self.domain_node_list as _:
            items = ["string", 42, {"key": "value"}, [1, 2, 3]]
            _.extend(items)
            
            assert _.items() == items

    def test_remove(self):                                             # Test removing items
        with self.domain_node_list as _:
            _.add("value1")
            _.add("value2")
            _.add("value1")  # Duplicate value
            
            assert _.remove("value1") is True
            items = _.items()
            assert len(items) == 2
            assert items.count("value1") == 1
            
            # Try removing non-existent value
            assert _.remove("non_existent") is False