from typing                                                             import Union, Dict, List, Optional, Any
from osbot_utils.utils.Files                                            import file_save
from osbot_utils.utils.Json                                             import json_dumps
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node__Dict   import Domain__MGraph__Json__Node__Dict
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node__List   import Domain__MGraph__Json__Node__List
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node__Value  import Domain__MGraph__Json__Node__Value
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Graph        import Domain__MGraph__Json__Graph
from mgraph_ai.mgraph.actions.MGraph__Export                            import MGraph__Export

class MGraph__Json__Export(MGraph__Export):                     # JSON export handler
    graph: Domain__MGraph__Json__Graph

    def to_dict(self) -> Union[Dict, List, Any]:                # Export to Python object
        root_content = self.graph.root_content()
        if not root_content:
            return None

        if isinstance(root_content, Domain__MGraph__Json__Node__Dict):
            return root_content.properties()
        elif isinstance(root_content, Domain__MGraph__Json__Node__List):
            return root_content.items()
        elif isinstance(root_content, Domain__MGraph__Json__Node__Value):
            return root_content.value

    def to_string(self, indent: Optional[int] = None) -> str:  # Export to JSON string
        data = self.to_dict()
        return json_dumps(data, indent=indent)

    def to_file(self, file_path: str, indent: Optional[int] = None) -> bool:  # Export to JSON file
        file_contents = self.to_string(indent=indent)
        if file_contents:
            file_save(contents=file_contents, path=file_path)
            return True
        return False
