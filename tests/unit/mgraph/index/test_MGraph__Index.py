from unittest                                               import TestCase
from mgraph_db.providers.simple.MGraph__Simple__Test_Data   import MGraph__Simple__Test_Data
from osbot_utils.utils.Objects                              import __
from osbot_utils.testing.Temp_File                          import Temp_File
from mgraph_db.mgraph.MGraph                                import MGraph
from osbot_utils.utils.Files                                import file_not_exists, file_exists
from mgraph_db.mgraph.actions.MGraph__Index                 import MGraph__Index
from mgraph_db.mgraph.schemas.Schema__MGraph__Index__Data   import Schema__MGraph__Index__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Node          import Schema__MGraph__Node
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge          import Schema__MGraph__Edge


class test_MGraph_Index(TestCase):

    def setUp(self):
        self.mgraph_index = MGraph__Index()

    def test__setUp(self):

        with self.mgraph_index as _:
            assert type(_           ) is MGraph__Index
            assert type(_.index_data) is Schema__MGraph__Index__Data
            assert _.json()           == { 'index_data' : { 'edges_to_nodes'                 : {} ,
                                                            'edges_by_type'                  : {} ,
                                                            'edges_types'                    : {} ,
                                                            'nodes_by_field'                 : {},
                                                            'nodes_by_type'                  : {} ,
                                                            'nodes_to_incoming_edges_by_type': {} ,
                                                            'nodes_to_incoming_edges'        : {} ,
                                                            'nodes_to_outgoing_edges'        : {} ,
                                                            'nodes_to_outgoing_edges_by_type': {} ,
                                                            'nodes_types'                    : {}}}

    def test_add_node(self):    # Test adding a node to the index
        node_to_add = Schema__MGraph__Node()

        with self.mgraph_index as _:
            _.add_node(node_to_add)

            # Verify node was added to type index
            assert node_to_add.node_type.__name__ in _.index_data.nodes_by_type
            assert node_to_add.node_id in _.index_data.nodes_by_type[node_to_add.node_type.__name__]
            assert node_to_add.node_id in _.index_data.nodes_to_outgoing_edges

    def test_add_edge(self):                                                                                            # Test adding an edge to the index
        node_1  = Schema__MGraph__Node()
        node_2  = Schema__MGraph__Node()
        edge    = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
        edge_id = edge.edge_config.edge_id

        with self.mgraph_index as _:
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge  )

            assert edge.edge_type.__name__ in _.index_data.edges_by_type                                                # Verify edge was added to type and node relationship indexes
            assert edge_id in _.index_data.edges_by_type          [edge.edge_type.__name__]
            assert edge_id in _.index_data.nodes_to_outgoing_edges[node_1.node_id         ]
            assert edge_id in _.index_data.nodes_to_incoming_edges[node_2.node_id         ]

    def test_remove_node(self):                                                                                         # Test removing a node from the index
        node_to_remove = Schema__MGraph__Node()

        with self.mgraph_index as _:
            _.add_node   (node_to_remove)
            _.remove_node(node_to_remove)

            assert node_to_remove.node_type.__name__ not in _.index_data.nodes_by_type                                  # Verify node was removed from type and node indexes
            assert node_to_remove.node_id            not in _.index_data.nodes_to_outgoing_edges
            assert node_to_remove.node_id            not in _.index_data.nodes_to_incoming_edges

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

            assert edge.edge_type.__name__ not in _.index_data.edges_by_type                                            # Verify edge was removed from type and node relationship indexes
            assert edge_id                 not in _.index_data.nodes_to_outgoing_edges.get(node_1.node_id, set())
            assert edge_id                 not in _.index_data.nodes_to_incoming_edges.get(node_2.node_id, set())

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
            assert _.index_data.obj()  == __(nodes_types                     = __(),
                                             edges_types                     = __(),
                                             nodes_to_outgoing_edges         = __(),
                                             nodes_to_incoming_edges         = __(),
                                             nodes_to_incoming_edges_by_type = __(),
                                             nodes_to_outgoing_edges_by_type = __(),
                                             edges_to_nodes                  = __(),
                                             nodes_by_type                   = __(),
                                             edges_by_type                   = __(),
                                             nodes_by_field                  = __())
            _.add_node(node_1)
            _.add_node(node_2)
            _.add_edge(edge_1)
            nodes_by_type = list(_.index_data.nodes_by_type['Schema__MGraph__Node'])            # we need to get this value since nodes_by_type is a list and the order can change
            assert node_1_id           in nodes_by_type
            assert node_2_id           in nodes_by_type
            assert _.index_data.json() == { 'edges_to_nodes'                 : { edge_1_id: [node_1_id, node_2_id]},
                                            'edges_by_type'                  : {'Schema__MGraph__Edge': [edge_1_id]},
                                            'edges_types'                    : { edge_1_id: 'Schema__MGraph__Edge'},
                                            'nodes_by_field'                 : {},
                                            'nodes_by_type'                  : {'Schema__MGraph__Node': nodes_by_type },
                                            'nodes_to_incoming_edges'        : { node_2_id: [edge_1_id],
                                                                                 node_1_id: []},
                                            'nodes_to_incoming_edges_by_type': { node_2_id: {'Schema__MGraph__Edge': [edge_1_id]}},
                                            'nodes_to_outgoing_edges'        : { node_2_id: [],
                                                                                 node_1_id: [edge_1_id]},
                                            'nodes_to_outgoing_edges_by_type': { node_1_id: {'Schema__MGraph__Edge': [edge_1_id]}},
                                            'nodes_types'                    : { node_1_id: 'Schema__MGraph__Node',
                                                                                 node_2_id: 'Schema__MGraph__Node'}}


    def test__index_data__from_simple_graph(self):
        simple_graph  = MGraph__Simple__Test_Data().create()
        with simple_graph.index() as _:
            assert len(_.edges_to_nodes         ()) == 2
            assert len(_.edges_by_type          ()) == 1
            assert len(_.nodes_by_field         ()) == 2              # BUG
            assert len(_.nodes_by_type          ()) == 1
            assert len(_.nodes_to_incoming_edges()) == 3
            assert len(_.nodes_to_outgoing_edges()) == 3

    def test_from_graph(self):                                                                      # Test creating index from graph using class method
        mgraph    = MGraph()
        node_1    = Schema__MGraph__Node()
        node_2    = Schema__MGraph__Node()
        edge_1    = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)
        node_1_id = node_1.node_id
        node_2_id = node_2.node_id
        edge_1_id = edge_1.edge_config.edge_id
        edge_1_type = edge_1.edge_type.__name__
        node_1_type = node_1.node_type.__name__

        with mgraph.edit() as _:
            _.add_node(node_1)                                                   # Add nodes and edges to graph
            _.add_node(node_2)
            _.add_edge(edge_1)
        with mgraph.data() as _:
            assert _.nodes_ids() == [node_1_id, node_2_id]
            assert _.edges_ids() == [edge_1_id           ]

        index         = MGraph__Index.from_graph(mgraph.graph)                                                # Create index from graph
        nodes_by_type = list(index.index_data.nodes_by_type['Schema__MGraph__Node'])
        assert node_1_id               in nodes_by_type
        assert node_2_id               in nodes_by_type
        assert index.index_data.json() ==  {  'edges_to_nodes'                 : { edge_1_id: [node_1_id, node_2_id] },
                                              'edges_by_type'                  : { edge_1_type: [edge_1_id]          },
                                              'edges_types'                    : { edge_1_id: 'Schema__MGraph__Edge'},
                                              'nodes_by_field'                 :  {}                                   ,
                                              'nodes_by_type'                  : { node_1_type: nodes_by_type        },
                                              'nodes_to_incoming_edges'        : { node_1_id: []                     ,
                                                                                   node_2_id: [edge_1_id]            },
                                              'nodes_to_incoming_edges_by_type': {node_2_id: {'Schema__MGraph__Edge': [edge_1_id]}},
                                              'nodes_to_outgoing_edges'        : { node_1_id: [edge_1_id]            ,
                                                                                   node_2_id: []                     },
                                             'nodes_to_outgoing_edges_by_type' : { node_1_id: {'Schema__MGraph__Edge': [edge_1_id]}},
                                             'nodes_types'                     : { node_1_id: 'Schema__MGraph__Node',
                                                                                   node_2_id: 'Schema__MGraph__Node'}}



    def test_save_to_file__and__from_file(self):                                                             # Test save and load functionality
        node_1 = Schema__MGraph__Node()
        node_2 = Schema__MGraph__Node()
        edge   = Schema__MGraph__Edge(from_node_id=node_1.node_id, to_node_id=node_2.node_id)

        with self.mgraph_index as _:
            _.add_node(node_1)                                                                      # Add nodes and edge to index
            _.add_node(node_2)
            _.add_edge(edge)

            with Temp_File(return_file_path=True, extension='json', create_file=False) as target_file:                   # temp file to use

                assert file_not_exists(target_file)
                _.save_to_file(target_file)                                                            # Save to temp file
                assert file_exists(target_file)

                # todo: find a way to make this more deterministic, the use of set() keeps causing everynow and then an CI pipeline error
                # loaded_index = MGraph__Index.from_file(target_file)                                     # Load index from file
                # loaded_index     .index_data.nodes_by_type['Schema__MGraph__Node'] = set(list(loaded_index     .index_data.nodes_by_type['Schema__MGraph__Node']))  # todo: find better way to handle this
                # self.mgraph_index.index_data.nodes_by_type['Schema__MGraph__Node'] = set(list(self.mgraph_index.index_data.nodes_by_type['Schema__MGraph__Node']))  #       we need to do this because the order of this 'set' object can change

                #assert loaded_index.json() == self.mgraph_index.json()                                  # confirm object as the save (original and loaded from disk)
                #assert loaded_index.obj () == self.mgraph_index.obj ()
