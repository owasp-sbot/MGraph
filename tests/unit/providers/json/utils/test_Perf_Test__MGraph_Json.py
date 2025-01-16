from unittest                                               import TestCase
from mgraph_ai.providers.json.utils.Perf_Test__MGraph_Json  import Perf_Test__MGraph_Json
from tests.unit.helpers.xml.rss.Test_Data__RSS__Feed        import TEST_DATA__TECH_NEWS__FEED_XML_JSON

URL__DBPEDIA__ZAP          = "https://dbpedia.org/data/ZAP.json"
URL__DBPEDIA__OWASP_ZAP    = "https://dbpedia.org/data/OWASP_ZAP.json"
URL__MY_FEEDS__HACKER_NEWS = "https://dev.myfeeds.ai/hacker-news/data-feed-current"
URL__MY_FEEDS__OPENAPI     = "https://dev.myfeeds.ai/openapi.json"
JSON__RSS_FEED__TEST_FEED  = TEST_DATA__TECH_NEWS__FEED_XML_JSON

class test_Perf_Test__MGraph_Json(TestCase):

    def setUp(self):
        self.perf_test = Perf_Test__MGraph_Json()

    def test_run_workflow__on_json(self):
        with self.perf_test as _:
            _.run_workflow__on_json(JSON__RSS_FEED__TEST_FEED)
            _.print()
            assert _.perf_test_duration.duration__total < 1

    def test_run_workflow__on_url(self):
        url = URL__DBPEDIA__ZAP
        with self.perf_test as _:
            _.run_workflow__on_url(url)
            _.print()
            assert _.perf_test_duration.duration__total < 3

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

# JSON__RSS_FEED__TEST_FEED  = TEST_DATA__TECH_NEWS__FEED_XML_JSON
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