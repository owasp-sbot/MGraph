from typing import Type
from mgraph_db.mgraph.actions.MGraph__Screenshot                      import MGraph__Screenshot
from mgraph_db.providers.json.actions.MGraph__Json__Export            import MGraph__Json__Export
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Graph      import Domain__MGraph__Json__Graph

from osbot_utils.type_safe.Type_Safe import Type_Safe

class MGraph__Json__Screenshot(MGraph__Screenshot):
    graph       : Domain__MGraph__Json__Graph
    export_class: Type[MGraph__Json__Export]

    def dot(self):
        dot_code         = self.export().to_dot().to_string()
        screenshot_bytes = self.dot_to_png(dot_code)
        return screenshot_bytes


# from mgraph_db_serverless.graph_engines.matplotlib.models.Model__Matplotlib__Render import Model__Matplotlib__Render
# from dataclasses                                                                    import asdict
#     def matplotlib(self):
#         render_config    = Model__Matplotlib__Render(graph_data=self.graph.json())
#         method_path      = PATH__RENDER_MERMAID
#         method_params    = asdict(render_config)
#         return self.execute_request(method_path, method_params)

    # def mermaid(self):
    #     mermaid_code     = self.export().to_mermaid().to_string()
    #     method_path      = PATH__RENDER_MERMAID
    #     method_params    = {'mermaid_code': mermaid_code}
    #     return self.execute_request(method_path, method_params)