from unittest                                                          import TestCase
from mgraph_db.providers.json.MGraph__Json                             import MGraph__Json

class test_MGraph__Json(TestCase):
    def setUp(self):                                                                          # Initialize test data
        self.mgraph = MGraph__Json()
        self.test_data = { "string" : "value"         ,
                           "number" : 42              ,
                           "boolean": True            ,
                           "null"   : None            ,
                           "array"  : [1, 2, 3]       ,
                           "object" : {"key": "value"}}

    def test_init(self):                                                                      # Test basic initialization
        assert type(self.mgraph          ) is MGraph__Json
        assert type(self.mgraph.data   ()) is not None
        assert type(self.mgraph.edit   ()) is not None
        assert type(self.mgraph.export ()) is not None
        assert type(self.mgraph.load()) is not None
        assert type(self.mgraph.storage()) is not None


    # def test_url(self):
    #     from osbot_utils.utils.Http import GET
    #     url = 'https://dbpedia.org/data/ZAP.json'
    #
    #     json_str = GET(url)
    #     self.mgraph.load().from_string(json_str)
    #     print()
    #     print(self.mgraph.export().to__dot())