from typing                                     import List, Dict, Any
from datetime                                   import datetime
from mgraph_db.providers.rss.MGraph__RSS_Item   import MGraph__RSS_Item
from mgraph_db.providers.json.MGraph__Json      import MGraph__Json
from osbot_utils.type_safe.Type_Safe            import Type_Safe


class MGraph__RSS_Feed(Type_Safe):                      # Wrapper for RSS feed operations"""
    mgraph : MGraph__Json
    channel     : Dict[str, Any]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.channel = self._get_channel()

    @property
    def title(self) -> str:
        """Get feed title"""
        return self._get_channel_property('title')

    @property
    def description(self) -> str:
        """Get feed description"""
        return self._get_channel_property('description')

    @property
    def link(self) -> str:
        """Get feed link"""
        return self._get_channel_property('link')

    @property
    def items(self) -> List[MGraph__RSS_Item]:
        """Get all feed items"""
        items = self.channel.get('item', [])
        if not isinstance(items, list):
            items = [items]
        return [MGraph__RSS_Item(node=item) for item in items]

    def recent_items(self, days: int = 7) -> List[MGraph__RSS_Item]:
        """Get items from the last N days"""
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
        return [
            item for item in self.items
            if item.pub_date and item.pub_date.timestamp() > cutoff
        ]

    def search(self, query: str) -> List[MGraph__RSS_Item]:
        """Search items by content"""
        query = query.lower()
        return [
            item for item in self.items
            if (item.title and query in item.title.lower()) or
               (item.description and query in item.description.lower())
        ]

    def categories(self) -> List[str]:
        """Get all unique categories"""
        categories = set()
        for item in self.items:
            categories.update(item.categories)
        return sorted(list(categories))

    def items_by_category(self, category: str) -> List[MGraph__RSS_Item]:
        """Get all items in a specific category"""
        return [
            item for item in self.items
            if category in item.categories
        ]

    def _get_channel(self) -> Dict[str, Any]:
        """Get channel data from graph"""
        with self.mgraph.graph as graph:
            root = graph.root()
            if root and isinstance(root, dict):
                return root.get('channel', {})
            return {}

    def _get_channel_property(self, name: str) -> Any: # Helper to get channel properties
        return self.channel.get(name)

