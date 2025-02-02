from osbot_utils.type_safe.Type_Safe                             import Type_Safe
from osbot_utils.utils.Files                                     import file_contents, file_exists
from osbot_utils.utils.Json                                      import json_loads
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Graph import Domain__MGraph__Json__Graph

class MGraph__Json__Load(Type_Safe):                                                                    # JSON import handler
    graph: Domain__MGraph__Json__Graph

    def from_string(self, json_str: str) -> Domain__MGraph__Json__Graph:                      # Import from JSON string
        data = json_loads(json_str)
        if data:
            return self.from_data(data)

    def from_data(self, data: dict) -> Domain__MGraph__Json__Graph:                            # Import from Python object
        self.graph.set_root_content(data)
        return self.graph

    def from_file(self, file_path: str) -> Domain__MGraph__Json__Graph:                       # Import from JSON file
        if file_exists(file_path):
            json_str = file_contents(file_path)
            return self.from_string(json_str)



