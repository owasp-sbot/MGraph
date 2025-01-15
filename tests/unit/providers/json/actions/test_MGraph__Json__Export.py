from unittest                               import TestCase
from osbot_utils.utils.Files                import file_exists, file_delete
from osbot_utils.utils.Json                 import json_loads
from mgraph_ai.providers.json.MGraph__Json  import MGraph__Json


class test_MGraph__Json__Export(TestCase):

    def setUp(self):                                                                          # Initialize test data
        self.mgraph = MGraph__Json()
        self.test_data = { "string" : "value"         ,
                           "number" : 42              ,
                           "boolean": True            ,
                           "null"   : None            ,
                           "array"  : [1, 2, 3]       ,
                           "object" : {"key": "value"}}

    def test_export_formats(self):                                                            # Test different export formats
        self.mgraph.load().from_dict(self.test_data)

        dict_export         = self.mgraph.export().to_dict()                                  # Test dict export
        str_export          = self.mgraph.export().to_string()                                # Test string export without indent
        str_export_indented = self.mgraph.export().to_string(indent=2)                        # Test string export with indent

        assert type(dict_export) is dict
        assert dict_export                      == self.test_data
        assert type(str_export)                 is str
        assert json_loads(str_export)           == self.test_data
        assert type(str_export_indented)        is str
        assert json_loads(str_export_indented)  == self.test_data
        assert len(str_export_indented)          > len(str_export)

    def test_file_operations(self):                                                 # Test file import/export
        file_path = "test.json"
        self.mgraph.load().from_dict(self.test_data)                             # Test export to file
        assert self.mgraph.export().to_file(str(file_path), indent=2) is True
        assert file_exists(file_path)                                 is True

        new_graph = MGraph__Json()                                                  # Test import from file
        imported  = new_graph.load().from_file(str(file_path))
        assert imported.root_content()                                is not None
        assert new_graph.export().to_dict()                           == self.test_data
        assert file_delete(file_path)                                 is True

    def test_error_handling(self):                                                  # Test error conditions
        assert self.mgraph.load().from_string("{invalid json}") is None
        assert self.mgraph.load().from_file("nonexistent.json") is None
        empty_graph = MGraph__Json()                                                # Test export with no content
        assert empty_graph.export().to_dict()                      is None
        assert empty_graph.export().to_file("/invalid/path")       is False      # Test file export to invalid path
