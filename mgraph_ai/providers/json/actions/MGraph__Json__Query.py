from typing                                                             import Dict, Any, Optional, List, Union
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node__Dict   import Domain__MGraph__Json__Node__Dict
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node__List   import Domain__MGraph__Json__Node__List
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node__Value  import Domain__MGraph__Json__Node__Value
from mgraph_ai.query.MGraph__Query                                      import MGraph__Query


class MGraph__Json__Query(MGraph__Query):

    def name(self, property_name: str) -> 'MGraph__Json__Query':              # Property access by name
        base_query = self.with_field('name', property_name)
        return self._wrap_base_query(base_query)

    def dict(self) -> Dict[str, Any]:                                         # Get current node as dictionary
        if not self.current_node_ids:
            return {}

        node = self.first()
        if isinstance(node, Domain__MGraph__Json__Node__Dict):
            return node.properties()
        return {}

    def list(self) -> List[Any]:                                              # Get current node as list
        if not self.current_node_ids:
            return []

        node = self.first()
        if isinstance(node, Domain__MGraph__Json__Node__List):
            return node.items()
        return []

    def value(self) -> Optional[Any]:                                         # Override base value() for JSON specifics
        if not self.current_node_ids:
            return None

        node = self.first()
        if isinstance(node, Domain__MGraph__Json__Node__Value):
            return node.value
        return None

    def __getitem__(self, key: Union[str, int]) -> 'MGraph__Json__Query':    # Array/dict access via [] notation
        if isinstance(key, int):
            return self._get_array_item(key)
        return self._get_dict_item(str(key))

    def _get_array_item(self, index: int) -> 'MGraph__Json__Query':
        if not self.current_node_ids:
            return self._empty_json_query()

        node = self.first()
        if not isinstance(node, Domain__MGraph__Json__Node__List):
            return self._empty_json_query()

        items = node.items()
        if 0 <= index < len(items):
            return self._wrap_value(items[index])
        return self._empty_json_query()

    def _get_dict_item(self, key: str) -> 'MGraph__Json__Query':
        if not self.current_node_ids:
            return self._empty_json_query()

        node = self.first()
        if not isinstance(node, Domain__MGraph__Json__Node__Dict):
            return self._empty_json_query()

        value = node.property(key)
        if value is not None:
            return self._wrap_value(value)
        return self._empty_json_query()

    def _wrap_value(self, value: Any) -> 'MGraph__Json__Query':
        new_query = self._empty_json_query()
        if isinstance(value, (Domain__MGraph__Json__Node__Dict,
                            Domain__MGraph__Json__Node__List,
                            Domain__MGraph__Json__Node__Value)):
            new_query.current_node_ids = {value.node_id}
            new_query.current_node_type = value.__class__.__name__
        return new_query

    def _empty_json_query(self) -> 'MGraph__Json__Query':
        return MGraph__Json__Query(mgraph_index=self.mgraph_index, mgraph_data=self.mgraph_data)

    def _wrap_base_query(self, base_query: MGraph__Query) -> 'MGraph__Json__Query':
        json_query = self._empty_json_query()
        json_query.current_node_ids = base_query.current_node_ids
        json_query.current_node_type = base_query.current_node_type
        return json_query