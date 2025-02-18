from typing                                                      import Type, Optional
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value        import Schema__MGraph__Node__Value
from mgraph_db.mgraph.schemas.Schema__MGraph__Value__Index__Data import Schema__MGraph__Value__Index__Data
from osbot_utils.helpers.Obj_Id                                  import Obj_Id
from osbot_utils.type_safe.Type_Safe                             import Type_Safe
from osbot_utils.utils.Dev                                       import pprint
from osbot_utils.utils.Misc                                      import str_md5

SIZE__VALUE_HASH = 10                                                                    # only use 10 chars from the md5 for the value (which is still 8 billion combinations

class MGraph__Index__Values(Type_Safe):
    index_data : Schema__MGraph__Value__Index__Data                                      # Value index data

    def add_value_node(self, node: Schema__MGraph__Node__Value) -> None:                # Add a value node to index
        if not node.node_data:
            raise ValueError("Node data is required for value nodes")

        value_hash = self.calculate_hash(value_type = node.node_data.value_type,
                                         value      = node.node_data.value     ,
                                         key        = node.node_data.key       )

        if value_hash in self.index_data.hash_to_node:                                  # Check uniqueness
            raise ValueError(f"Value with hash {value_hash} already exists")

        self.index_data.hash_to_node[value_hash  ] = node.node_id                       # Add to main indexes
        self.index_data.node_to_hash[node.node_id] = value_hash

        if node.node_data.value_type not in self.index_data.values_by_type:             # Add to type indexes
            self.index_data.values_by_type[node.node_data.value_type] = set()
        self.index_data.values_by_type[node.node_data.value_type].add(value_hash)
        self.index_data.type_by_value [value_hash               ] = node.node_data.value_type

    def get_node_id_by_hash(self, value_hash: str) -> Optional[Obj_Id]:                         # returns node_id that matches value's hash
        return self.index_data.hash_to_node.get(value_hash)

    def get_node_id_by_value(self, value_type: Type, value: str, key:str='') -> Optional[Obj_Id]:           # returns node_id that matches value
        value_hash = self.calculate_hash(value_type=value_type, value=value, key=key)
        return self.get_node_id_by_hash(value_hash)

    def remove_value_node(self, node: Schema__MGraph__Node__Value) -> None:             # Remove from all indexes
        value_hash = self.index_data.node_to_hash.get(node.node_id)
        if value_hash:
            # Remove from main indexes
            del self.index_data.hash_to_node[value_hash]
            del self.index_data.node_to_hash[node.node_id]

            # Remove from type indexes
            if node.node_data.value_type in self.index_data.values_by_type:
                self.index_data.values_by_type[node.node_data.value_type].discard(value_hash)
                if not self.index_data.values_by_type[node.node_data.value_type]:
                    del self.index_data.values_by_type[node.node_data.value_type]

            if value_hash in self.index_data.type_by_value:
                del self.index_data.type_by_value[value_hash]

    def calculate_hash(self, value_type: Type, value: str, key:str='') -> str:                      # Calculate value hash
        if value_type is None:
            raise ValueError("In MGraph__Index__Values.calculate_hash , value_type was None")
        type_name = f"{value_type.__module__}.{value_type.__name__}"         # Get full type path
        if key:
            hash_data = f"{type_name}::{key}::{value}"                       # Combine with key and value
        else:
            hash_data = f"{type_name}::{value}"                              # Combine with value
        return str_md5(hash_data)[:SIZE__VALUE_HASH]


    def print__values_index_data(self):
        pprint(self.index_data.json())