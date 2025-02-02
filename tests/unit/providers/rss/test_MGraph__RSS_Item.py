from unittest                                 import TestCase
from datetime                                 import datetime, timezone
from mgraph_db.providers.rss.MGraph__RSS_Item import MGraph__RSS_Item

class test_MGraph__RSS_Item(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample_date = "Mon, 22 Jan 2025 15:30:00 +0000"
        cls.item_data   = { 'title'      : "Test Article"                            ,
                            'description': "This is a test article description"      ,
                            'link'       : "https://example.com/article"             ,
                            'pubDate'    : cls.sample_date                           ,
                            'category'   : ["tech", "news"]                          ,
                            'guid'       : "12345" }
        cls.item = MGraph__RSS_Item(node= cls.item_data)

    def test_init(self):
        with self.item as _:
            assert type(_) is MGraph__RSS_Item
            assert _.node  == self.item_data

    def test_title(self):
        assert self.item.title        == "Test Article"

    def test_description(self):
        assert self.item.description  == "This is a test article description"

    def test_link(self):
        assert self.item.link         == "https://example.com/article"

    def test_pub_date(self):
        expected_date = datetime(2025, 1, 22, 15, 30, tzinfo=timezone.utc)
        assert self.item.pub_date     == expected_date

    def test_pub_date_invalid(self):
        item_data = self.item_data.copy()
        item_data['pubDate'] = "Invalid Date"
        item = MGraph__RSS_Item(node=item_data)
        assert item.pub_date          is None

    def test_pub_date_missing(self):
        item_data = self.item_data.copy()
        del item_data['pubDate']
        item = MGraph__RSS_Item(node=item_data)
        assert item.pub_date          is None

    def test_categories_list(self):
        assert self.item.categories   == ["tech", "news"]

    def test_categories_single(self):
        item_data = self.item_data.copy()
        item_data['category'] = "tech"
        item = MGraph__RSS_Item(node=item_data)
        assert item.categories        == ["tech"]

    def test_categories_missing(self):
        item_data = self.item_data.copy()
        del item_data['category']
        item = MGraph__RSS_Item(node=item_data)
        assert item.categories        == []

    def test_get_property_missing(self):
        assert self.item.get_property('nonexistent') is None

    def test_to_dict(self):
        expected = {
            'title'      : "Test Article"                        ,
            'description': "This is a test article description"  ,
            'link'       : "https://example.com/article"        ,
            'pubDate'    : self.sample_date                     ,
            'category'   : ["tech", "news"]                     ,
            'guid'       : "12345"
        }
        assert self.item.to_dict()    == expected