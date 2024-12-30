from typing                             import Dict, Any
from osbot_utils.helpers.Random_Guid    import Random_Guid
from osbot_utils.base_classes.Type_Safe import Type_Safe


class MGraph__Node(Type_Safe):
    node_id    : Random_Guid
    attributes : Dict[str, Any]
    key        : str
    label      : str

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'[Graph Node] {self.key}'

    def set_key(self, value: str):
        self.key = value
        return self

    def set_label(self, value: str):
        self.label = value
        return self