from unittest                                        import TestCase
from mgraph_ai.providers.rss.MGraph__RSS             import MGraph_RSS
from tests.unit.helpers.xml.rss.Test_Data__RSS__Feed import TEST_DATA__TECH_NEWS__FEED_XML


class test_MGraph_RSS(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mgraph_rss = MGraph_RSS()

    def test__init__(self):
        with self.mgraph_rss as _:
            assert type(_) is MGraph_RSS

    def test_feed_url__to__json(self):
        url = 'https://feeds.feedburner.com/TheHackersNews'
        with self.mgraph_rss as _:
            result = _.feed_url__to__json(url)
            assert result.get('channel').get('title') == 'The Hacker News'

    def test_feed_xml__to__json(self):
        feed_xml = TEST_DATA__TECH_NEWS__FEED_XML
        with self.mgraph_rss as _:
            result = _.feed_xml__to__json(feed_xml)
            assert result.get('channel').get('title') == 'Tech News Daily'
