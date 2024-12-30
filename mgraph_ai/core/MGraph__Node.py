from typing import Dict, Any

from osbot_utils.helpers.Safe_Id import Safe_Id

from osbot_utils.helpers.Random_Guid import Random_Guid

from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.utils.Misc             import random_id


class MGraph__Node(Type_Safe):
    node_id    : Random_Guid
    attributes : Dict[str, Any]
    key        : str
    label      : str

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     if not self.key:
    #         self.key = random_id()
    #     if not self.label:
    #         self.label = self.key

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