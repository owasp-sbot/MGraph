from unittest                                               import TestCase
from mgraph_ai.providers.json.utils.Perf_Test__MGraph_Json  import Perf_Test__MGraph_Json


URL__DBPEDIA__ZAP          = "https://dbpedia.org/data/ZAP.json"
URL__DBPEDIA__OWASP_ZAP    = "https://dbpedia.org/data/OWASP_ZAP.json"
URL__MY_FEEDS__HACKER_NEWS = "https://dev.myfeeds.ai/hacker-news/data-feed-current"
URL__MY_FEEDS__OPENAPI     = "https://dev.myfeeds.ai/openapi.json"

class test_Perf_Test__MGraph_Json(TestCase):

    def setUp(self):
        self.perf_test = Perf_Test__MGraph_Json()

    def test_run_workflow__on_json(self):
        with self.perf_test as _:
            _.run_workflow__on_json(TEST_DATA__TECH_NEWS__FEED_XML_JSON)
            _.print()
            assert _.perf_test_duration.duration__total < 2   # shower in GitHub Actions (locally it's around 0.5)

    def test_run_workflow__on_url(self):
        url = URL__DBPEDIA__ZAP
        with self.perf_test as _:
            _.run_workflow__on_url(url)
            _.print()
            assert _.perf_test_duration.duration__total < 6 # shower in GitHub Actions (locally it's around 1.5)

    # # contains=['models__from_edges', 'edges', 'add_node', 'new_dict_node', 'add_property'],
    # @trace_calls(contains=['models__from_edges', 'edges' , 'add_node'],
    #              show_duration=True, duration_padding=110,
    #              show_class   =True)
    # def test_trace(self):
    #     mgraph_json = MGraph__Json()
    #
    #     json_example = { "string" : "value"         ,
    #                      "number" : 42              ,
    #                      "boolean": True            ,
    #                      "null"   : None            ,
    #                      "array"  : [1, 2, 3]       ,
    #                      "object" : {"key": "value"}}
    #     source_json = {"a": 1, "b": 2, 'c': {'d': 4, 'e': 5},
    #                    "f": ['x', 'y', 'z'],
    #                    #'c': json_example,
    #                    #'d': [json_example, json_example],
    #                    }
    #
    #     mgraph_json.load().from_json(source_json)


### CURRENT STATS (16th Jan 2024)

# URL__DBPEDIA__ZAP "https://dbpedia.org/data/ZAP.json"
#
# ----- Pef Test Results ----
#
#   Target URL: https://dbpedia.org/data/ZAP.json
#   Nodes     : 101
#   Edges     : 100
#   Dot Code  : 14614
#
# duration__get_source_json: 0.087
# duration__mgraph_parse   : 0.88
# duration__dot_creation   : 0.28


# URL__DBPEDIA__OWASP_ZAP = "https://dbpedia.org/data/OWASP_ZAP.json"
#
# ----- Pef Test Results ----
#
#   Target URL: https://dbpedia.org/data/OWASP_ZAP.json
#   Nodes     : 686
#   Edges     : 685
#   Dot Code  : 104619
#
# duration__get_source_json: 0.152
# duration__mgraph_parse   : 36.692
# duration__dot_creation   : 11.842

# URL__MY_FEEDS_HACKER_NEWS = "https://dev.myfeeds.ai/hacker-news/data-feed-current"
#
# ----- Perf Test Results ----
#
#   Target URL: https://dbpedia.org/data/ZAP.json
#   Nodes     : 101
#   Edges     : 100
#   Dot Code  : 14614
#
# duration__get_source_json: 0.078
# duration__mgraph_parse   : 0.867
# duration__dot_creation   : 0.283
# ---------------------------------
# duration__total          : 1.228
# ---------------------------------

# URL__MY_FEEDS__OPENAPI = "https://dev.myfeeds.ai/openapi.json"
#
# ----- Pef Test Results ----
#
#   Target URL: https://dev.myfeeds.ai/openapi.json
#   Nodes     : 776
#   Edges     : 775
#   Dot Code  : 111630
#
# duration__get_source_json: 0.144
# duration__mgraph_parse   : 54.95
# duration__dot_creation   : 16.728

# target_json = TEST_DATA__TECH_NEWS__FEED_XML_JSON
#
# ----- Perf Test Results ----
#
#   Target URL:
#   Nodes     : 63
#   Edges     : 62
#   Dot Code  : 8957
#
# duration__get_source_json: 0.0
# duration__mgraph_parse   : 0.337
# duration__dot_creation   : 0.155
# ---------------------------------
# duration__total          : 0.492
# ---------------------------------



TEST_DATA__TECH_NEWS__FEED_XML_JSON = { 'channel': { 'description': 'Latest Technology News',
                                                     'extensions': {},
                                                     'image'     : None,
                                                     'items': [ { 'categories': [],
                                                                  'content': {},
                                                                  'creator': 'None',
                                                                  'description': 'Major advancement in artificial '
                                                                                 'intelligence research',
                                                                  'enclosure' : None,
                                                                  'extensions': { 'author': 'editor@technewsdaily.example.com',
                                                                                  'enclosure': { 'length': '12216320',
                                                                                                 'type': 'image/jpeg',
                                                                                                 'url': 'https://example.com/ai-image.jpg'}},
                                                                  'guid': '2e0985da-6a11-54be-b557-39402ba4a8ad',
                                                                  'link': 'https://technewsdaily.example.com/2024/12/ai-breakthrough.html',
                                                                  'pubDate': 'Wed, 04 Dec 2024 22:53:00 +0530',
                                                                  'thumbnail': {},
                                                                  'title': 'New AI Breakthrough'}],
                                                     'language'         : 'en-us',
                                                     'last_build_date'  : 'Thu, 05 Dec 2024 01:33:01 +0530',
                                                     'link'             : 'https://technewsdaily.example.com',
                                                     'title'            : 'Tech News Daily',
                                                     'update_frequency' : '1'              ,
                                                     'update_period'    : 'hourly'         },
                                        'extensions': {},
                                        'namespaces': {},
                                        'version': '2.0'}