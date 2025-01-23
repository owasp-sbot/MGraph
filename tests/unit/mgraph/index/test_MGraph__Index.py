from unittest                                               import TestCase
from osbot_utils.utils.Dev                                  import pprint
from osbot_utils.utils.Files                                import temp_file, file_not_exists
from osbot_utils.utils.Objects                              import type_full_name, __
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config  import Schema__MGraph__Edge__Config
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph__Data   import Schema__MGraph__Graph__Data
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node          import Schema__MGraph__Node
from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data    import Schema__MGraph__Node__Data
from mgraph_ai.mgraph.MGraph                                import MGraph
from mgraph_ai.mgraph.domain.Domain__MGraph__Graph          import Domain__MGraph__Graph
from mgraph_ai.mgraph.models.Model__MGraph__Graph           import Model__MGraph__Graph
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge          import Schema__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Graph         import Schema__MGraph__Graph
from mgraph_ai.mgraph.index.MGraph__Index                   import MGraph__Index
from mgraph_ai.mgraph.utils.MGraph__Static__Graph           import MGraph__Static__Graph

class test_MGraph_Index(TestCase):

    # def setUp(cls):
    #     cls.static_graph      = MGraph__Static__Graph()
    #     cls.linear_graph      = cls.static_graph.linear_graph()
    #     cls.linear_graph_data = cls.linear_graph.graph.graph.model.data
    #     cls.mgraph_index      = MGraph__Index(graph=cls.linear_graph_data)
    #
    #
    # def test__setUpClass(self):
    #     assert type(self.static_graph                       ) is MGraph__Static__Graph
    #     assert type(self.linear_graph                       ) is MGraph__Static__Graph
    #     assert type(self.linear_graph.graph                 ) is MGraph
    #     assert type(self.linear_graph.graph.graph           ) is Domain__MGraph__Graph
    #     assert type(self.linear_graph.graph.graph.model     ) is Model__MGraph__Graph
    #     assert type(self.linear_graph.graph.graph.model.data) is Schema__MGraph__Graph
    #     assert type(self.mgraph_index                       ) is MGraph__Index
    #     assert type(self.mgraph_index.graph                 ) is Schema__MGraph__Graph
    #
    #     with self.linear_graph.graph.data() as _:
    #         graph_id  = _.graph_id ()
    #         nodes_ids = _.nodes_ids()
    #         edges_ids = _.edges_ids()
    #
    #     with self.mgraph_index as _:
    #         assert _.graph == self.linear_graph.graph.graph.model.data
    #
    #         assert _.json() == { 'graph': { 'edges'     : { edges_ids[0]: { 'edge_config' : {'edge_id': edges_ids[0] }              ,
    #                                                                         'edge_data'   : {}                                          ,
    #                                                                         'edge_type'   : type_full_name(Schema__MGraph__Edge)        ,
    #                                                                         'from_node_id': nodes_ids[0]                                ,
    #                                                                         'to_node_id'  : nodes_ids[1]                                },
    #                                                         edges_ids[1]: { 'edge_config' : {'edge_id': edges_ids[1] }                  ,
    #                                                                         'edge_data'   : {}                                          ,
    #                                                                         'edge_type'   : type_full_name(Schema__MGraph__Edge)        ,
    #                                                                         'from_node_id': nodes_ids[1]                                ,
    #                                                                         'to_node_id'  : nodes_ids[2]                                }},
    #                                         'graph_data': {}                                                                            ,
    #                                         'graph_id'  : graph_id                                                                      ,
    #                                         'graph_type': type_full_name(Schema__MGraph__Graph)                                         ,
    #                                         'nodes'     : { nodes_ids[0]: { 'node_data'   : {}                                          ,
    #                                                                         'node_id'     : nodes_ids[0]                                ,
    #                                                                         'node_type'   : type_full_name(Schema__MGraph__Node)        },
    #                                                         nodes_ids[1]: { 'node_data'   : {}                                          ,
    #                                                                         'node_id'     : nodes_ids[1]                                ,
    #                                                                         'node_type'   : type_full_name(Schema__MGraph__Node)        },
    #                                                         nodes_ids[2]: { 'node_data'   : {}                                          ,
    #                                                                         'node_id'     : nodes_ids[2]                                ,
    #                                                                         'node_type'   : type_full_name(Schema__MGraph__Node)        }},
    #                                         'schema_types': { 'edge_config_type'          : type_full_name(Schema__MGraph__Edge__Config ),
    #                                                           'edge_type'                 : type_full_name(Schema__MGraph__Edge         ),
    #                                                           'graph_data_type'           : type_full_name(Schema__MGraph__Graph__Data  ),
    #                                                           'node_data_type'            : type_full_name(Schema__MGraph__Node__Data   ),
    #                                                           'node_type'                 : type_full_name(Schema__MGraph__Node         )}},
    #                              'index': { 'data'       : { 'edge_to_nodes'              : {}                                          ,
    #                                                          'edges_by_attribute'         : {}                                          ,
    #                                                          'edges_by_type'              : {}                                          ,
    #                                                          'nodes_by_attribute'         : {}                                          ,
    #                                                          'nodes_by_type'              : {}                                          ,
    #                                                          'nodes_to_incoming_edges'    : {}                                          ,
    #                                                          'nodes_to_outgoing_edges'    : {}                                          }}}

    def setUp(self):
        self.mgraph_index = MGraph__Index()

    def test__setUp(self):
        graph_id  = self.mgraph_index.graph.graph_id

        with self.mgraph_index as _:
            assert _.json() == { 'graph': { 'edges'       : {                                                                             },
                                            'graph_data'  : {}                                                                            ,
                                            'graph_id'    : graph_id                                                                      ,
                                            'graph_type'  : type_full_name(Schema__MGraph__Graph)                                         ,
                                            'nodes'       : {                                                                             },
                                            'schema_types': { 'edge_config_type'          : type_full_name(Schema__MGraph__Edge__Config ),
                                                              'edge_type'                 : type_full_name(Schema__MGraph__Edge         ),
                                                              'graph_data_type'           : type_full_name(Schema__MGraph__Graph__Data  ),
                                                              'node_data_type'            : type_full_name(Schema__MGraph__Node__Data   ),
                                                              'node_type'                 : type_full_name(Schema__MGraph__Node         )}},
                                 'index': { 'data'       : { 'edge_to_nodes'              : {}                                          ,
                                                             'edges_by_attribute'         : {}                                          ,
                                                             'edges_by_type'              : {}                                          ,
                                                             'nodes_by_attribute'         : {}                                          ,
                                                             'nodes_by_type'              : {}                                          ,
                                                             'nodes_to_incoming_edges'    : {}                                          ,
                                                             'nodes_to_outgoing_edges'    : {}}}}

    def test_add_node(self):    # Test adding a node to the index
        node_to_add = Schema__MGraph__Node()

        with self.mgraph_index as _:
            _.add_node(node_to_add)

            # Verify node was added to type index
            assert node_to_add.node_type.__name__ in _.index.data.nodes_by_type
            assert node_to_add.node_id in _.index.data.nodes_by_type[node_to_add.node_type.__name__]
            assert node_to_add.node_id in _.index.data.nodes_to_outgoing_edges

    def test_add_edge(self):                                                                                            # Test adding an edge to the index
        node_1  = Schema__MGraph__Node()
        node_2  = Schema__MGraph__Node()
        edge    = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
        edge_id = edge.edge_config.edge_id

        with self.mgraph_index as _:
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge  )

            assert edge.edge_type.__name__ in _.index.data.edges_by_type                                                # Verify edge was added to type and node relationship indexes
            assert edge_id in _.index.data.edges_by_type          [edge.edge_type.__name__]
            assert edge_id in _.index.data.nodes_to_outgoing_edges[node_1.node_id         ]
            assert edge_id in _.index.data.nodes_to_incoming_edges[node_2.node_id         ]

    def test_remove_node(self):                                                                                         # Test removing a node from the index
        node_to_remove = Schema__MGraph__Node()

        with self.mgraph_index as _:
            _.add_node   (node_to_remove)
            _.remove_node(node_to_remove)

            assert node_to_remove.node_type.__name__ not in _.index.data.nodes_by_type                                  # Verify node was removed from type and node indexes
            assert node_to_remove.node_id            not in _.index.data.nodes_to_outgoing_edges
            assert node_to_remove.node_id            not in _.index.data.nodes_to_incoming_edges

    def test_remove_edge(self):                                                                                         # Test removing an edge from the index
        node_1  = Schema__MGraph__Node()
        node_2  = Schema__MGraph__Node()
        edge    = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
        edge_id = edge.edge_config.edge_id

        with self.mgraph_index as _:
            _.add_node   (node_1)
            _.add_node   (node_2)
            _.add_edge   (edge  )
            _.remove_edge(edge  )

            assert edge.edge_type.__name__ not in _.index.data.edges_by_type                                            # Verify edge was removed from type and node relationship indexes
            assert edge_id                 not in _.index.data.nodes_to_outgoing_edges.get(node_1.node_id, set())
            assert edge_id                 not in _.index.data.nodes_to_incoming_edges.get(node_2.node_id, set())

    def test_get_methods(self):                                                                                         # Test various get methods of the index
        node_1  = Schema__MGraph__Node()
        node_2  = Schema__MGraph__Node()
        edge    = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
        edge_id = edge.edge_config.edge_id

        with self.mgraph_index as _:
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge  )

            assert node_1.node_id in _.get_nodes_by_type(Schema__MGraph__Node)                                          # Test get methods
            assert edge_id        in _.get_edges_by_type(Schema__MGraph__Edge)

    def test_json(self):
        node_1 = Schema__MGraph__Node()
        node_2 = Schema__MGraph__Node()
        edge_1 = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
        node_1_id = node_1.node_id
        node_2_id = node_2.node_id
        edge_1_id = edge_1.edge_config.edge_id

        with self.mgraph_index as _:
            assert _.index.obj()  == __(data=__(nodes_to_outgoing_edges = __(),
                                                nodes_to_incoming_edges = __(),
                                                edge_to_nodes           = __(),
                                                nodes_by_type           = __(),
                                                edges_by_type           = __(),
                                                nodes_by_attribute      = __(),
                                                edges_by_attribute      = __()))
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge_1)
            assert _.index.json() == { 'data': { 'edge_to_nodes'          : { edge_1_id: [node_1_id, node_2_id]},
                                                 'edges_by_attribute'     : {},
                                                 'edges_by_type'          : {'Schema__MGraph__Edge': [edge_1_id]},
                                                 'nodes_by_attribute'     : {},
                                                 'nodes_by_type'          : {'Schema__MGraph__Node': [node_1_id, node_2_id]},
                                                 'nodes_to_incoming_edges': { node_2_id: [edge_1_id],
                                                                              node_1_id: []},
                                                 'nodes_to_outgoing_edges': { node_2_id: [],
                                                                              node_1_id: [edge_1_id]}}}


    def test_save_and_load_index(self):                                                                                 # Test saving and loading the index to/from a file
        node_1 = Schema__MGraph__Node()
        node_2 = Schema__MGraph__Node()
        edge   = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

        with self.mgraph_index as _:
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge)

            temp_filename = temp_file('.json')                                                                          # Save to a temp file
            assert file_not_exists(temp_filename)
            _.save_to_file(temp_filename)



        # # Load from the file
        # loaded_index = MGraph__Index.load_from_file(self.linear_graph_data, temp_filename)
        #
        # # Verify loaded index has the same content
        # assert len(loaded_index.index.data.nodes_by_type) == len(self.mgraph_index.index.data.nodes_by_type)
