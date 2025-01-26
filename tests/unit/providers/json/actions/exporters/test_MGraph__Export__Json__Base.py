from unittest                                                               import TestCase
from osbot_utils.utils.Files                                                import file_exists, file_delete
from mgraph_ai.providers.json.MGraph__Json                                  import MGraph__Json
from mgraph_ai.providers.json.actions.exporters.MGraph__Json__Export__Base  import MGraph__Export__Json__Base, Export__Json__Node_Type, Export__Json__Format_Error


class Mock_Exporter(MGraph__Export__Json__Base):                                         # Mock exporter for testing base functionality
    def process_node(self, node):                                               # Track method calls
        self.last_processed = ('node', node)
        return 'test_node_id'

    def process_edge(self, from_id, to_id, type_):                             # Track method calls
        self.last_processed = ('edge', from_id, to_id, type_)

    def process_value_node(self, node):                                        # Track method calls
        self.last_processed = ('value', node)
        return 'test_value_id'

    def process_array_node(self, node):                                        # Track method calls
        self.last_processed = ('array', node)
        return 'test_array_id'

    def process_object_node(self, node):                                       # Track method calls
        self.last_processed = ('object', node)
        return 'test_object_id'

    def format_output(self):                                                   # Return simple test output
        return "test_output"

class test_MGraph__Export__Json__Base(TestCase):

    def setUp(self):                                                           # Initialize test data
        self.mgraph = MGraph__Json()
        self.exporter = Mock_Exporter(self.mgraph.graph)
        self.test_data = { "string" : "value"         ,
                           "number" : 42              ,
                           "boolean": True            ,
                           "null"   : None            ,
                           "array"  : [1, 2, 3]       ,
                           "object" : {"key": "value"}}

    def test_init(self):                                                       # Test initialization
        assert type(self.exporter)                               is Mock_Exporter
        assert type(self.exporter.graph)                         == type(self.mgraph.graph)
        assert type(self.exporter.context)                       is dict
        assert 'nodes'                    in self.exporter.context
        assert 'edges'                    in self.exporter.context
        assert 'counters'                 in self.exporter.context

    def test_node_type_detection(self):                                        # Test node type detection
        self.mgraph.load().from_data(self.test_data)
        root = self.mgraph.graph.root_content()

        assert self.exporter.get_node_type(root)                == Export__Json__Node_Type.OBJECT

        array_data = [1, 2, 3]
        self.mgraph.load().from_data(array_data)
        array_root = self.mgraph.graph.root_content()
        assert self.exporter.get_node_type(array_root)          == Export__Json__Node_Type.ARRAY

        value_data = "test"
        self.mgraph.load().from_data(value_data)
        value_root = self.mgraph.graph.root_content()
        assert self.exporter.get_node_type(value_root)          == Export__Json__Node_Type.VALUE

    def test_value_formatting(self):                                           # Test value formatting
        assert self.exporter.format_value(None)                  == "null"
        assert self.exporter.format_value(True)                  == "true"
        assert self.exporter.format_value(False)                 == "false"
        assert self.exporter.format_value(42)                    == "42"
        assert self.exporter.format_value(3.14)                  == "3.14"
        assert self.exporter.format_value("test")                == '"test"'

    def test_id_generation(self):                                             # Test ID generation
        assert self.exporter.generate_node_id("node")            == "node_0"
        assert self.exporter.generate_node_id("node")            == "node_1"
        assert self.exporter.generate_node_id("edge")            == "edge_0"
        assert self.exporter.generate_node_id("property")        == "property_0"

    def test_object_export(self):                                             # Test object export
        self.mgraph.load().from_data({"key": "value"})
        output = self.exporter.to_string()
        assert output                                            == "test_output"
        assert self.exporter.last_processed[0]                   == "object"

    def test_array_export(self):                                              # Test array export
        self.mgraph.load().from_data([1, 2, 3])
        output = self.exporter.to_string()
        assert output                                            == "test_output"
        assert self.exporter.last_processed[0]                   == "array"

    def test_value_export(self):                                              # Test value export
        self.mgraph.load().from_data("test")
        output = self.exporter.to_string()
        assert output                                            == "test_output"
        assert self.exporter.last_processed[0]                   == "value"

    def test_empty_graph(self):                                               # Test empty graph handling
        output = self.exporter.to_string()
        assert output                                            == ""

    def test_error_handling(self):                                            # Test error handling
        def failing_process():
            raise Exception("Test error")

        self.exporter.process_object_node = failing_process
        self.mgraph.load().from_data({"key": "value"})

        with self.assertRaises(Export__Json__Format_Error):
            self.exporter.to_string()

        with self.assertRaises(Export__Json__Format_Error):
            self.exporter.to_file("nonexistent/path/file.txt")

    def test_file_export(self):                                               # Test file export with mock
        file_name = 'test.txt'
        self.mgraph.load().from_data(self.test_data)
        assert self.exporter.to_file(file_name)    is True
        assert file_exists(file_name) is True
        assert file_delete(file_name) is True