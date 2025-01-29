from unittest                                 import TestCase

from osbot_utils.utils.Dev import pprint

from mgraph_ai.providers.json.MGraph__Json    import MGraph__Json
from mgraph_ai.providers.rss.MGraph__RSS_Feed import MGraph__RSS_Feed
from mgraph_ai.providers.rss.MGraph__RSS_Item import MGraph__RSS_Item

class test_MGraph__RSS_Feed(TestCase):
    @classmethod
    def setUpClass(cls):

        import pytest
        pytest.skip("Fix tests once MGraph_RSS is fixed")
        cls.mgraph       = MGraph__Json()
        cls.channel_data = {
            'title'      : "Test Feed"                              ,
            'description': "A test RSS feed"                        ,
            'link'       : "https://example.com/feed"              ,
            'item'       : [
                {
                    'title'      : "Article 1"                      ,
                    'description': "First article"                  ,
                    'link'       : "https://example.com/article1"  ,
                    'pubDate'    : "Mon, 22 Jan 2025 15:30:00 +0000",
                    'category'   : ["tech"]
                },
                {
                    'title'      : "Article 2"                      ,
                    'description': "Second article"                 ,
                    'link'       : "https://example.com/article2"  ,
                    'pubDate'    : "Mon, 21 Jan 2025 10:00:00 +0000",
                    'category'   : ["news"]
                }
            ]
        }
        
        with cls.mgraph.load() as _:
            _.from_json({'channel': cls.channel_data})
            
        cls.feed = MGraph__RSS_Feed(mgraph=cls.mgraph)

    def test_init(self):
        with self.feed as _:
            assert type(_) is MGraph__RSS_Feed
            assert _.mgraph is self.mgraph
            assert type(_.channel) is dict

    def test_raw_mgraph(self):
        with self.mgraph as _:
            pprint(_.json())

    def test_export_to_dot(self):
        with self.mgraph as _:
            print()
            print(_.export().to_dot().to_string())

    def test_title(self):
        assert self.feed.title         == "Test Feed"
        
    def test_description(self):
        assert self.feed.description   == "A test RSS feed"
        
    def test_link(self):
        assert self.feed.link          == "https://example.com/feed"
        
    def test_items(self):
        items = self.feed.items
        assert len(items)              == 2
        assert all(isinstance(item, MGraph__RSS_Item) for item in items)
        assert items[0].title          == "Article 1"
        assert items[1].title          == "Article 2"
        
    def test_items_single(self):
        # Test when 'item' is a single dict instead of list
        channel_data = self.channel_data.copy()
        channel_data['item'] = channel_data['item'][0]
        
        with self.mgraph.edit() as edit:
            edit.set_root_content({'channel': channel_data})
            
        feed = MGraph__RSS_Feed(node=self.mgraph)
        items = feed.items
        assert len(items)              == 1
        assert items[0].title          == "Article 1"
        
    def test_recent_items(self):
        items = self.feed.recent_items(days=7)
        assert len(items)              == 2  # Both items are recent
        
        # Test with older date
        channel_data = self.channel_data.copy()
        channel_data['item'][0]['pubDate'] = "Mon, 1 Jan 2024 15:30:00 +0000"
        
        with self.mgraph.edit() as edit:
            edit.set_root_content({'channel': channel_data})
            
        feed = MGraph__RSS_Feed(node=self.mgraph)
        items = feed.recent_items(days=7)
        assert len(items)              == 1
        
    def test_search(self):
        # Search in title
        items = self.feed.search("Article 1")
        assert len(items)              == 1
        assert items[0].title          == "Article 1"
        
        # Search in description
        items = self.feed.search("Second")
        assert len(items)              == 1
        assert items[0].title          == "Article 2"
        
        # Case insensitive search
        items = self.feed.search("ARTICLE")
        assert len(items)              == 2
        
    def test_categories(self):
        categories = self.feed.categories()
        assert categories              == ["news", "tech"]
        
    def test_items_by_category(self):
        tech_items = self.feed.items_by_category("tech")
        assert len(tech_items)         == 1
        assert tech_items[0].title     == "Article 1"
        
        news_items = self.feed.items_by_category("news")
        assert len(news_items)         == 1
        assert news_items[0].title     == "Article 2"
        
    def test_get_channel_empty_root(self):
        with self.mgraph.edit() as edit:
            edit.set_root_content(None)
            
        feed = MGraph__RSS_Feed(node=self.mgraph)
        assert feed.channel == {}