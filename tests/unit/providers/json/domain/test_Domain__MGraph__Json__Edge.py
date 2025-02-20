from unittest                                                   import TestCase
from mgraph_db.mgraph.domain.Domain__MGraph__Edge               import Domain__MGraph__Edge
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge              import Schema__MGraph__Edge
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Edge import Domain__MGraph__Json__Edge
from osbot_utils.utils.Objects                                  import __, type_full_name


class test_Domain__MGraph__Json__Edge(TestCase):

    def test__init__(self):
        with Domain__MGraph__Json__Edge() as _:
            assert isinstance(_, Domain__MGraph__Edge)
            assert _.obj() == __(edge  = __(data = __( edge_id      = _.edge_id                           ,
                                                       edge_data    = __()                                ,
                                                       edge_type    = type_full_name(Schema__MGraph__Edge),
                                                       from_node_id = _.from_node_id()                    ,
                                                       to_node_id   = _.to_node_id  ()                    )) ,
                                 graph = _.graph.obj())