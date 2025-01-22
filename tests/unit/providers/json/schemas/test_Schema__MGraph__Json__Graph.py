import re
from unittest import TestCase

import pytest

from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config import Schema__MGraph__Edge__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph__Data import Schema__MGraph__Graph__Data
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data import Schema__MGraph__Node__Data
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Edge import Schema__MGraph__Json__Edge
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node import Schema__MGraph__Json__Node
from osbot_utils.utils.Objects import __, type_full_name

from osbot_utils.utils.Dev import pprint

from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Graph import Schema__MGraph__Json__Graph


class test_Schema__MGraph__Json__Graph(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.schema_graph = Schema__MGraph__Json__Graph()

    def test__init__(self):
        with self.schema_graph as _:
            assert _.obj() == __(graph_data   = __(root_id=None),
                                 graph_id     = _.graph_id  ,
                                 graph_type   = type_full_name(Schema__MGraph__Json__Graph),
                                 schema_types = __(edge_type        = type_full_name(Schema__MGraph__Json__Edge   ),
                                                   edge_config_type = type_full_name(Schema__MGraph__Edge__Config ),
                                                   graph_data_type  = type_full_name(Schema__MGraph__Graph__Data  ),
                                                   node_type        = type_full_name(Schema__MGraph__Json__Node   ),
                                                   node_data_type   = type_full_name(Schema__MGraph__Node__Data   )),
                                 edges        = __() ,
                                 nodes        = __() )

    def test__bug__from_json(self):
        with self.schema_graph as _:
            error_message = "Invalid type for attribute 'graph_type'. Expected 'typing.Type[ForwardRef('Schema__MGraph__Graph')]' but got '<class 'str'>'"
            with pytest.raises(ValueError, match=re.escape(error_message)):
                Schema__MGraph__Json__Graph.from_json(_.json())
