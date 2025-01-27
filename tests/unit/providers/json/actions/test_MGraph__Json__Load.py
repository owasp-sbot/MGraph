from unittest                                                           import TestCase
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node__List   import Domain__MGraph__Json__Node__List
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node__Value  import Domain__MGraph__Json__Node__Value
from osbot_utils.utils.Json                                             import json_loads
from mgraph_ai.providers.json.MGraph__Json                              import MGraph__Json
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node__Dict   import Domain__MGraph__Json__Node__Dict

class test_MGraph__Json__Load(TestCase):
    def setUp(self):                                                                          # Initialize test data
        self.mgraph = MGraph__Json()
        self.test_data = { "string" : "value"         ,
                           "number" : 42              ,
                           "boolean": True            ,
                           "null"   : None            ,
                           "array"  : [1, 2, 3]       ,
                           "object" : {"key": "value"}}

    def test_import_from_dict(self):                                                          # Test importing from dict
        graph = self.mgraph.load().from_data(self.test_data)
        root_content = graph.root_content()
        assert isinstance(root_content, Domain__MGraph__Json__Node__Dict)
        assert root_content.property("string" ) == "value"
        assert root_content.property("number" )  == 42
        assert root_content.property("boolean") is True
        assert root_content.property("null"   ) is None

    def test_import_from_string(self):                                                        # Test importing from JSON string
        json_str     = '{"key": "value", "list": [1,2,3]}'
        graph        = self.mgraph.load().from_string(json_str)
        root_content = graph.root_content()
        assert isinstance(root_content, Domain__MGraph__Json__Node__Dict)
        assert root_content.property("key" ) == "value"
        assert root_content.property("list") == [1, 2, 3]

    def test_export_to_dict(self):                                                            # Test exporting to dict
        self.mgraph.load().from_data(self.test_data)
        exported = self.mgraph.export().to_dict()
        assert exported            == self.test_data
        assert exported["string" ] == "value"
        assert exported["number" ] == 42
        assert exported["boolean"] is True
        assert exported["null"   ] is None
        assert exported["array"  ] == [1, 2, 3]
        assert exported["object" ] == {"key": "value"}

    def test_export_to_string(self):                                                          # Test exporting to JSON string
        self.mgraph.load().from_data(self.test_data)
        exported = self.mgraph.export().to_string()
        assert json_loads(exported) == self.test_data

    def test_primitive_values(self):                                                          # Test handling primitive values
        values = ["string", 42, 3.14, True, False, None ]
        for value in values:
            graph        = self.mgraph.load().from_data(value)
            root_content = graph.root_content()
            assert isinstance(root_content, Domain__MGraph__Json__Node__Value)
            assert root_content.value              == value
            assert self.mgraph.export().to_dict()  == value

    def test_array_handling(self):                                                            # Test array operations
        array_data = [1, "two", {"three": 3}, [4, 5]]
        graph = self.mgraph.load().from_data(array_data)
        root_content = graph.root_content()
        assert isinstance(root_content, Domain__MGraph__Json__Node__List)
        items = root_content.items()
        assert items[0]                       == 1
        assert items[1]                       == "two"
        assert items[2]                       == {"three": 3}
        assert items[3]                       == [4, 5]
        assert self.mgraph.export().to_dict() == array_data

    def test_nested_structures(self):                                                         # Test nested JSON structures
        nested_data  = {"level1": {"level2": {"level3": {"array": [1, 2, {"key": "value"}],
                                                         "value": "nested"               }}}}
        graph        = self.mgraph.load().from_data(nested_data)
        root_content = graph.root_content()
        assert isinstance(root_content, Domain__MGraph__Json__Node__Dict)
        assert self.mgraph.export().to_dict() == nested_data

    def test_empty_structures(self):                                                          # Test empty JSON structures
        empty_data   = { "empty_object" : {} ,
                         "empty_array"  : [] ,
                         "empty_string" : "" }
        graph        = self.mgraph.load().from_data(empty_data)
        root_content = graph.root_content()
        assert isinstance(root_content, Domain__MGraph__Json__Node__Dict)
        assert self.mgraph.export().to_dict() == empty_data