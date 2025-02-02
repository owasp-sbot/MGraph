from typing                                              import List, Dict, Any, Optional, Type
from datetime                                            import datetime
from osbot_utils.helpers.xml.rss.RSS__Feed               import RSS__Feed
from osbot_utils.type_safe.Type_Safe                     import Type_Safe
from mgraph_db.providers.json.MGraph__Json               import MGraph__Json

class MGraph__RSS(Type_Safe):
    rss_feed : RSS__Feed
    graph    : MGraph__Json


    # RSS Channel Properties
    @property
    def title(self) -> str:                                                  # Get feed title
        with self.graph.edit() as edit:
            root = edit.root()
            return root.get_property('channel').get_property('title')

    @property
    def description(self) -> str:                                           # Get feed description
        with self.graph.edit() as edit:
            root = edit.root()
            return root.get_property('channel').get_property('description')

    @property
    def items(self) -> List[Dict[str, Any]]:                               # Get all items
        with self.graph.edit() as edit:
            root = edit.root()
            return root.get_property('channel').get_property('items')

    def find_items_by_category(self, category: str) -> List[Dict]:         # Find items by category
        return [item for item in self.items
                if category in item.get('categories', [])]

    def find_items_by_date_range(self, start: datetime,
                                     end  : datetime) -> List[Dict]:        # Find items in date range
        return [item for item in self.items
                if start <= datetime.fromtimestamp(item['pub_date']['timestamp_utc']) <= end]

    def find_items_by_author(self, author: str) -> List[Dict]:            # Find items by author
        return [item for item in self.items
                if item.get('creator') == author]

    def get_all_categories(self) -> List[str]:                            # Get unique categories
        categories = set()
        for item in self.items:
            categories.update(item.get('categories', []))
        return sorted(list(categories))

    def get_item_by_guid(self, guid: str) -> Optional[Dict]:              # Find item by GUID
        for item in self.items:
            if item.get('guid') == guid:
                return item
        return None

    def to_json(self) -> str:                                             # Export as JSON
        return self.graph.json()

    def to_rss(self) -> str:                                              # Export as RSS XML
        # Implement RSS XML serialization
        raise NotImplementedError("RSS XML export not yet implemented")

    def load_rss(self, rss_feed: RSS__Feed):
        self.rss_feed = rss_feed
        self.graph.load().from_data(rss_feed.json())