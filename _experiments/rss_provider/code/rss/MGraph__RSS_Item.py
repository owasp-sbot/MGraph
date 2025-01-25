from typing                          import Optional, List, Dict, Any
from datetime                        import datetime, timezone
from osbot_utils.type_safe.Type_Safe import Type_Safe


class MGraph__RSS_Item(Type_Safe):                         # Represents a single RSS feed item
    node : dict

    @property
    def title(self) -> str:                         # Get item title
        return self.get_property('title')

    @property
    def description(self) -> str:                   # Get item description/content
        return self.get_property('description')

    @property
    def link(self) -> str:                          # Get item link
        return self.get_property('link')

    @property
    def pub_date(self) -> Optional[datetime]:       # Get publication date
        date_str = self.get_property('pubDate')
        if date_str:
            # Parse RSS date format
            try:
                return datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
            except ValueError:
                return None
        return None

    @property
    def categories(self) -> List[str]:                           # Get item categories
        cats = self.get_property('category')
        if isinstance(cats, list):
            return cats
        elif cats:
            return [cats]
        return []

    def get_property(self, name: str) -> Any:           # Helper to get properties with proper null checking
        return self.node.get(name)


    def to_dict(self) -> Dict[str, Any]:                # Convert item to dictionary representation
        return { 'title': self.title,
                 'description': self.description,
                 'link': self.link,
                 'pubDate': self.get_property('pubDate'),
                 'category': self.categories,
                 'guid': self.get_property('guid')   }