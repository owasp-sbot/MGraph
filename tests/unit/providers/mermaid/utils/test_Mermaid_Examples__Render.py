from unittest import TestCase

import requests

from mgraph_ai.providers.mermaid.utils.Mermaid__Random_Graph import create_test_mermaid_graph
from osbot_utils.utils.Files import save_bytes_as_file

from osbot_utils.utils.Dev import pprint

from mgraph_ai.providers.mermaid.utils.Mermaid_Examples__FlowChart import Mermain_Examples__FlowChart


class test_Mermaid_Examples__Render(TestCase):

    @classmethod
    def setUpClass(cls):
        import pytest
        pytest.skip("fix test so that it doesn't run agains a live server")
        cls.examples = Mermain_Examples__FlowChart()

    def render_mermaid_code(self, mermaid_code):
        json_code       = {  "mermaid_code": mermaid_code }
        url              = "http://0.0.0.0:7770/web_root/render-mermaid"
        response        = requests.post(url, json=json_code)

        screenshot_bytes = response.content
        save_bytes_as_file(screenshot_bytes, '/tmp/mermaid-serverless.png')

    def test_example_1__a_node_default(self):

        mermaid_code = self.examples.example_1__a_node_default
        mermaid_code = self.examples.example_5__direction__from_top_to_bottom
        mermaid_code = self.examples.example_14__node_shapes_a_hexagon_node
#         mermaid_code = """\
# sequenceDiagram
#     Alice->>+John: Hello John, how are you?
#     Alice->>+John: John, can you hear me?
#     John-->>-Alice: Hi Alice, I can hear you!
#     John-->>-Alice: I feel great!
# """
        #mermaid_code = create_test_mermaid_graph(3,4).code()
        #pprint(mermaid_code)
        self.render_mermaid_code(mermaid_code)


