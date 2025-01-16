from typing                                         import Union
from mgraph_ai.providers.json.MGraph__Json          import MGraph__Json
from osbot_utils.context_managers.capture_duration  import capture_duration
from osbot_utils.utils.Http                         import GET_json
from osbot_utils.type_safe.Type_Safe                import Type_Safe

class Model__Perf_Test__Duration(Type_Safe):
    duration__get_source_json : float
    duration__mgraph_parse    : float
    duration__dot_creation    : float
    duration__total           : float

class Perf_Test__MGraph_Json(Type_Safe):
    perf_test_duration : Model__Perf_Test__Duration
    source_json        : Union[str, list, dict]
    mgraph_json        : MGraph__Json
    target_url         : str
    dot_code           : str

    def setup__get_source_json_from_url(self):
        with capture_duration() as duration:
            self.source_json = GET_json(self.target_url)
        self.perf_test_duration.duration__get_source_json = duration.seconds
        self.perf_test_duration.duration__total          += duration.seconds

        return self

    def step__create_mgraph(self):
        with capture_duration() as duration:
            self.mgraph_json.load().from_json(self.source_json)
        self.perf_test_duration.duration__dot_creation = duration.seconds
        self.perf_test_duration.duration__total       += duration.seconds
        return self

    def step__create_dot(self):
        with capture_duration() as duration:
            self.dot_code = self.mgraph_json.export().to_dot().to_string()
        self.perf_test_duration.duration__mgraph_parse = duration.seconds
        self.perf_test_duration.duration__total       += duration.seconds
        return self

    def run_workflow__on_url(self, target_url):
        self.target_url = target_url
        (self.setup__get_source_json_from_url ()
             .step__create_mgraph             ()
             .step__create_dot                ())

    def run_workflow__on_json(self, source_json):
        self.source_json = source_json
        (self.step__create_mgraph()
             .step__create_dot   ())

    def print(self):
        print()
        print("----- Perf Test Results ----")
        print()
        print(f"  Target URL: {self.target_url}")
        print(f"  Nodes     : {len(self.mgraph_json.graph.nodes_ids())}")
        print(f"  Edges     : {len(self.mgraph_json.graph.edges_ids())}")
        print(f"  Dot Code  : {len(self.dot_code)}")
        print()
        print(f"duration__get_source_json: {self.perf_test_duration.duration__get_source_json}")
        print(f"duration__mgraph_parse   : {self.perf_test_duration.duration__mgraph_parse}")
        print(f"duration__dot_creation   : {self.perf_test_duration.duration__dot_creation}")
        print('---------------------------------')
        print(f"duration__total          : {self.perf_test_duration.duration__total:.3f}")
        print('---------------------------------')
        print()

