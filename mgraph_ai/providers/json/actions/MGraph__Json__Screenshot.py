import requests
from mgraph_ai.providers.json.actions.MGraph__Json__Export            import MGraph__Json__Export
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Graph      import Domain__MGraph__Json__Graph
from osbot_utils.utils.Files                                          import file_create_from_bytes
from osbot_utils.utils.Http                                           import url_join_safe
from osbot_utils.utils.Env                                            import get_env, not_in_github_action

from osbot_utils.type_safe.Type_Safe import Type_Safe

ENV_NAME__URL__MGRAPH_AI_SERVERLESS     = 'URL__MGRAPH_AI_SERVERLESS'
PATH__RENDER_MATPLOTLIB                 = '/matplotlib/render-graph'
PATH__RENDER_MERMAID                    = '/web_root/render-mermaid'
PATH__RENDER_DOT                        = '/graphviz/render-dot'
DEFAULT__FILE_NAME__SCREENSHOT__SAVE_TO = './mgraph-screenshot.png'
DEFAULT__URL__LOCAL__MGRAPH_AI_API      = 'http://localhost:8080'

class MGraph__Json__Screenshot(Type_Safe):
    graph       : Domain__MGraph__Json__Graph
    target_file : str = None

    def handle_response(self, response):
        if response.status_code == 200:
            screenshot_bytes = response.content
            if self.target_file and screenshot_bytes:
                file_create_from_bytes(self.target_file, screenshot_bytes)
            return screenshot_bytes

    def execute_request(self, method_path, method_params):
        target_url       = self.url__render_method(method_path)
        response         = requests.post(target_url, json=method_params)
        screenshot_bytes = self.handle_response(response)
        return screenshot_bytes

    def export(self):
        return MGraph__Json__Export(graph=self.graph)

    def dot(self):
        dot_code         = self.export().to_dot().to_string()
        screenshot_bytes = self.create_screenshot__from__dot_code(dot_code)
        return screenshot_bytes

    def dot__just_ids(self):
        dot_code         = self.export().to__dot()
        screenshot_bytes = self.create_screenshot__from__dot_code(dot_code)
        return screenshot_bytes

    def dot__just_values(self):
        dot_code         = self.export().to__dot(show_value=True, show_edge_ids=False)
        screenshot_bytes = self.create_screenshot__from__dot_code(dot_code)
        return screenshot_bytes

    def dot__just_types(self):
        dot_code = self.export().to__dot_types()
        screenshot_bytes = self.create_screenshot__from__dot_code(dot_code)
        return screenshot_bytes

    def dot__schema(self):
        dot_code = self.export().to__dot_schema()
        screenshot_bytes = self.create_screenshot__from__dot_code(dot_code)
        return screenshot_bytes

    def create_screenshot__from__dot_code(self, dot_code):
        method_path   = PATH__RENDER_DOT
        method_params = {'dot_source': dot_code}
        return self.execute_request(method_path, method_params)

# from mgraph_ai_serverless.graph_engines.matplotlib.models.Model__Matplotlib__Render import Model__Matplotlib__Render
# from dataclasses                                                                    import asdict
#     def matplotlib(self):
#         render_config    = Model__Matplotlib__Render(graph_data=self.graph.json())
#         method_path      = PATH__RENDER_MERMAID
#         method_params    = asdict(render_config)
#         return self.execute_request(method_path, method_params)

    def mermaid(self):
        mermaid_code     = self.export().to_mermaid().to_string()
        method_path      = PATH__RENDER_MERMAID
        method_params    = {'mermaid_code': mermaid_code}
        return self.execute_request(method_path, method_params)

    def save(self):
        return self.save_to(DEFAULT__FILE_NAME__SCREENSHOT__SAVE_TO)

    def save_to(self, target_file):
        self.target_file = target_file
        return self

    def url__render_method(self, path):
        return url_join_safe(self.url__render_server(), path)

    def url__render_server(self):
        url = get_env(ENV_NAME__URL__MGRAPH_AI_SERVERLESS)
        if url is None and not_in_github_action():
            url = DEFAULT__URL__LOCAL__MGRAPH_AI_API
        return url