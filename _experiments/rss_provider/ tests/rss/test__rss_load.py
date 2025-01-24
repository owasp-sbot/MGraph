from unittest import TestCase

from osbot_utils.helpers.xml.rss.RSS__Feed__Parser import RSS__Feed__Parser

from mgraph_ai.providers.rss.MGraph__RSS import MGraph__RSS
from osbot_utils.utils.Dev import pprint

from osbot_utils.utils.Http import GET


class test_rss_load(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mgraph_rss = MGraph__RSS()

    def test_load_from_url(self):
        url = 'https://feeds.feedburner.com/TheHackersNews'
        xml_data = GET(url)
        xml_dict = self.mgraph_rss.xml_feed_to_dict(xml_data)
        rss_feed = RSS__Feed__Parser().from_dict(xml_dict)
        pprint(rss_feed.json())

