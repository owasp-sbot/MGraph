from unittest                                             import TestCase

from osbot_utils.context_managers.print_duration import print_duration

from osbot_utils.utils.Dev import pprint

from mgraph_ai.mgraph.index.MGraph__Query import MGraph__Query
from mgraph_ai.providers.json.MGraph__Json                import MGraph__Json
from mgraph_ai.providers.json.actions.MGraph__Json__Query import MGraph__Json__Query
from mgraph_ai.mgraph.index.MGraph__Index                 import MGraph__Index
from mgraph_ai.mgraph.actions.MGraph__Data                import MGraph__Data
from osbot_utils.type_safe.Type_Safe                      import Type_Safe
from osbot_utils.utils.Objects                            import base_types

class test_MGraph__Json__Query(TestCase):

    @classmethod
    def setUpClass(cls):
        import pytest
        pytest.skip("test needs fixing, after MGraph__Json__Query is refactored")

    def setUp(self):
        self.mgraph_json = MGraph__Json()
        self.test_data = { "string"  : "value"                                ,
                           "number"  : 42                                     ,
                           "object"  : { "nested": True                       ,
                                        "list"   : [1, 2, {"item": "value"}]} ,
                           "array"   : ["a", "b", {"key": "value"}]           }
        self.mgraph_json.load().from_json(self.test_data)
        self.mgraph_index = MGraph__Index.from_graph( graph        = self.mgraph_json.graph)
        self.mgraph_data  = MGraph__Data            ( graph        = self.mgraph_json.graph)
        self.json_query   = MGraph__Json__Query     ( mgraph_index = self.mgraph_index,
                                                      mgraph_data  = self.mgraph_data)

    def test_init(self):
        with self.json_query as _:
            assert type(_)                           is MGraph__Json__Query
            assert base_types(_)                     == [MGraph__Query, Type_Safe, object]
            assert self.json_query.mgraph_data       == self.mgraph_data
            assert self.json_query.mgraph_index      == self.mgraph_index
            assert self.json_query.current_node_ids  == set()
            assert self.json_query.current_node_type is None

            assert _.count()                         == 0

        with self.json_query.mgraph_index as _:
            assert _.stats() == {'index_data': { 'edge_to_nodes'         : 23                                                        ,
                                                 'edges_by_field'        : {}                                                        ,
                                                 'edges_by_type'         : { 'Schema__MGraph__Json__Edge'         : 23}             ,
                                                 'node_edge_connections' : { 'avg_incoming_edges'                 : 1               ,
                                                                             'avg_outgoing_edges'                 : 1               ,
                                                                             'max_incoming_edges'                 : 1               ,
                                                                             'max_outgoing_edges'                 : 4               ,
                                                                             'total_nodes'                        : 24              },
                                                 'nodes_by_field'        : { 'name'                               : { 'array'  : 1   ,
                                                                                                                      'item'    : 1  ,
                                                                                                                      'key'     : 1  ,
                                                                                                                      'list'    : 1  ,
                                                                                                                      'nested'  : 1  ,
                                                                                                                      'number'  : 1  ,
                                                                                                                      'object'  : 1  ,
                                                                                                                      'string'  : 1  },
                                                                            'value'                               : { True     : 2   ,
                                                                                                                      2        : 1   ,
                                                                                                                      42       : 1   ,
                                                                                                                      'a'      : 1   ,
                                                                                                                      'b'      : 1   ,
                                                                                                                      'value'  : 3   },
                                                                            'value_type'                          : { str  : 5      ,
                                                                                                                      bool : 1      ,
                                                                                                                      int  : 3      }},
                                                 'nodes_by_type'         : {'Schema__MGraph__Json__Node'          : 1                ,
                                                                            'Schema__MGraph__Json__Node__Dict'    : 4                ,
                                                                            'Schema__MGraph__Json__Node__List'    : 2                ,
                                                                            'Schema__MGraph__Json__Node__Property': 8                ,
                                                                            'Schema__MGraph__Json__Node__Value'   : 9                }}}

    def test_property_access(self):
        query = self.json_query

        with print_duration():
            with query.name('string') as _:
                assert type(_) is MGraph__Json__Query
                assert len(_.current_node_ids) == 1
                pprint(_.current_edges())
                pprint(_.current_nodes()[0].node.json())
        with print_duration():
            with query.name('string') as _:
                assert type(_) is MGraph__Json__Query
                assert len(_.current_node_ids) == 1
                pprint(_.current_edges())
                pprint(_.current_nodes()[0].node.json())
        #pprint(query_result.mgraph_index.json())
        return
        assert query.name('string').value() == "value"
        assert query.name('number').value() == 42
        assert query.name('object').name('nested').value() is True

    def test_array_access(self):
        query = self.json_query

        assert query.array[0].value()  == "a"
        assert query.array[1].value()  == "b"
        assert query.array[2].dict()   == {"key": "value"}
        assert query.array[99].value() is None                    # Out of bounds access

    def test_nested_structure(self):
        query = self.json_query

        assert query.object.list.list()     == [1, 2, {"item": "value"}]
        assert query.object.list[2].dict()  == {"item": "value"}
        assert query.object.list[2].item.value() == "value"

    def test_missing_values(self):
        query = self.json_query

        assert query.non_existent.exists()         is False
        assert query.non_existent.value()          is None
        assert query.string.nested.value()         is None
        assert query.string.list()                 == []         # Non-list returns empty
        assert query.number.dict()                 == {}         # Non-dict returns empty

    def test_type_conversion(self):
        query = self.json_query

        object_data = query.object.dict()
        assert object_data == {
            "nested": True,
            "list": [1, 2, {"item": "value"}]
        }

        array_data = query.array.list()
        assert array_data == ["a", "b", {"key": "value"}]

    def test_chained_operations(self):
        query = self.json_query

        result = (query.object
                      .list[2]
                      .item
                      .value())

        assert result == "value"

        result = (query.array
                      .filter(lambda n: isinstance(n, dict))
                      .first())

        assert result == {"key": "value"}