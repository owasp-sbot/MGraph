from unittest                                               import TestCase
from mgraph_db.mgraph.actions.exporters.MGraph__Export__Dot import MGraph__Export__Dot, MGraph__Export__Dot__Config
from mgraph_db.mgraph.domain.Domain__MGraph__Graph          import Domain__MGraph__Graph
from mgraph_db.mgraph.models.Model__MGraph__Graph           import Model__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph         import Schema__MGraph__Graph
from mgraph_db.providers.simple.MGraph__Simple__Test_Data   import MGraph__Simple__Test_Data
from osbot_utils.utils.Objects                              import __


class test_MGraph__Export__Dot(TestCase):

    def setUp(self):                                                                    # Initialize test environment
        self.simple_graph = MGraph__Simple__Test_Data().create()
        self.nodes_ids    = self.simple_graph.nodes_ids()
        self.edges_ids    = self.simple_graph.edges_ids()
        self.domain_graph = self.simple_graph.graph
        self.exporter     = MGraph__Export__Dot(graph=self.domain_graph)               # Create DOT exporter

    def test_init(self):                                                               # Test initialization
        config = MGraph__Export__Dot__Config(show_value    = True    ,
                                            show_edge_ids  = False   ,
                                            font_name     = "Times" ,
                                            font_size     = 12      )
        exporter = MGraph__Export__Dot(graph=self.domain_graph, config=config)

        assert exporter.graph                == self.domain_graph
        assert exporter.config.show_value    is True
        assert exporter.config.show_edge_ids is False
        assert exporter.config.font_name     == "Times"
        assert exporter.config.font_size     == 12

        assert exporter.obj() == __(graph       = self.domain_graph.obj()   ,
                                    context     = __( nodes         = __()                        ,
                                                      edges         = __()                        ,
                                                      counters      = __(node=0, edge=0, other=0)),
                                    config      = __( show_value    = True                        ,
                                                      show_edge_ids = False                       ,
                                                      font_name     = 'Times'                     ,
                                                      font_size     = 12                          ,
                                                      rank_sep      = 0.8                         ),
                                    on_add_node = None ,
                                    on_add_edge = None )

    def test_create_node_data(self):                                                   # Test node data creation
        node_id = self.nodes_ids[0]                                                    # Get first node (Node 1)
        node_data = self.exporter.create_node_data(self.domain_graph.node(node_id))

        assert node_data['id']           == str(node_id)
        assert 'value="A"'               in node_data['attrs']
        assert 'name="Node 1"'           in node_data['attrs']

        # Test with show_value=True
        self.exporter.config.show_value = True
        node_data = self.exporter.create_node_data(self.domain_graph.node(node_id))
        assert 'label="A"'               in node_data['attrs']

    def test_create_edge_data(self):                                                   # Test edge data creation
        edge_1_id = self.edges_ids[0]
        node_1_id = self.nodes_ids[0]
        node_2_id = self.nodes_ids[1]
        edge_data = self.exporter.create_edge_data(self.domain_graph.edge(edge_1_id))

        assert edge_data['id']     == str(edge_1_id)
        assert edge_data['source'] == str(node_1_id)
        assert edge_data['target'] == str(node_2_id)
        assert edge_data['type']   == 'Schema__MGraph__Edge'

    def test_format_output(self):                                                      # Test DOT output formatting
        self.exporter.process_graph()                                                  # Process graph first
        dot_output = self.exporter.format_output()

        assert 'digraph {'            in dot_output
        assert str(self.nodes_ids[0]) in dot_output
        assert str(self.nodes_ids[1]) in dot_output
        assert str(self.edges_ids[0]) in dot_output
        assert '->'                   in dot_output
        assert '}'                    in dot_output

        assert dot_output == ('digraph {\n'
                              f'  "{self.nodes_ids[0]}" [value="A", name="Node 1"]\n'
                              f'  "{self.nodes_ids[1]}" [value="B", name="Node 2"]\n'
                              f'  "{self.nodes_ids[2]}" [value="C", name="Node 3"]\n'
                              f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[1]}" [label="  {self.edges_ids[0]}"]\n'
                              f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[2]}" [label="  {self.edges_ids[1]}"]\n'
                              '}')

    def test_to_types_view(self):                                                      # Test types view generation
        types_view = self.exporter.to_types_view()

        assert 'digraph {'               in types_view
        assert 'fontname="Arial"'        in types_view
        assert 'shape=box'               in types_view
        assert 'style="rounded,filled"'  in types_view
        assert 'fillcolor=lightblue'     in types_view
        assert str(self.nodes_ids[0])    in types_view
        assert str(self.nodes_ids[1])    in types_view
        assert '->'                      in types_view

        # Verify the complete output
        expected_output = ('digraph {\n'
                          '  graph [fontname="Arial", ranksep=0.8]\n'
                          '  node  [fontname="Arial"]\n'
                          '  edge  [fontname="Arial", fontsize=10]\n'
                          f'  "{self.nodes_ids[0]}" [shape=box, style="rounded,filled", fillcolor=lightblue, label="Schema  Simple  Node", value="A", name="Node 1"]\n'
                          f'  "{self.nodes_ids[1]}" [shape=box, style="rounded,filled", fillcolor=lightblue, label="Schema  Simple  Node", value="B", name="Node 2"]\n'
                          f'  "{self.nodes_ids[2]}" [shape=box, style="rounded,filled", fillcolor=lightblue, label="Schema  Simple  Node", value="C", name="Node 3"]\n'
                          f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[1]}" [label="  Edge"]\n'
                          f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[2]}" [label="  Edge"]\n'
                          '}')
        assert types_view == expected_output


    def test_to_schema_view(self):                                                     # Test schema view generation
        schema_view = self.exporter.to_schema_view()

        expected_output = ('digraph {\n'
                          '  graph [fontname="Arial", ranksep=0.8]\n'
                          '  node  [fontname="Arial"]\n'
                          '  edge  [fontname="Arial", fontsize=10]\n'
                          '  "Schema  Simple  Node" [shape=box, style="rounded,filled", fillcolor=lightblue, label="Schema  Simple  Node", value="A", name="Node 1"]\n'
                          '  "Schema  Simple  Node" -> "Schema  Simple  Node" [label="  Edge"]\n'
                          '}')
        assert schema_view == expected_output


    def test_fix_schema_name(self):                                                    # Test schema name cleaning
        value = "Schema__MGraph__Test__Node__Value"
        fixed = self.exporter.fix_schema_name(value)
        assert fixed == "Test  Node  Value"

    def test_header_generation(self):                                                  # Test header generation
        basic_header = self.exporter.get_header()
        assert basic_header == ['digraph {']

        styled_header = self.exporter.get_styled_header()
        assert len(styled_header) == 4
        assert 'fontname="Arial"' in styled_header[1]
        assert 'ranksep=0.8'      in styled_header[1]
        assert 'node'             in styled_header[2]
        assert 'edge'             in styled_header[3]

    def test_empty_graph(self):                                                        # Test handling of empty graph
        empty_schema = Schema__MGraph__Graph(nodes      = {}                   ,
                                            edges      = {}                   ,
                                            graph_type = Schema__MGraph__Graph)
        empty_model  = Model__MGraph__Graph (data       = empty_schema        )
        empty_domain = Domain__MGraph__Graph(model      = empty_model         )
        empty_export = MGraph__Export__Dot  (graph      = empty_domain        )
        empty_export.process_graph()                                                   # Process graph first

        dot_output = empty_export.format_output()
        assert dot_output == 'digraph {\n}'

    def test_custom_config(self):                                                      # Test custom configuration
        config = MGraph__Export__Dot__Config(show_value    = True     ,
                                             show_edge_ids  = False   ,
                                             font_name     = "Courier",
                                             font_size     = 14       ,
                                             rank_sep      = 1.2      )

        exporter = MGraph__Export__Dot(graph=self.domain_graph, config=config)
        exporter.process_graph()                                                       # Process graph first
        output = exporter.format_output()

        # With show_value=True, should include label attributes
        assert 'label="A"' in output                                                   # First node's value

        # With show_edge_ids=False, should not include edge IDs in labels
        for edge_id in self.edges_ids:
            assert f'label="  {edge_id}"' not in output

        styled_output = exporter.to_types_view()
        assert 'fontname="Courier"' in styled_output
        assert 'fontsize=14'        in styled_output
        assert 'ranksep=1.2'        in styled_output

    def test__mgraph_export(self):
        with self.simple_graph.export() as _:
            assert _.to__dot_types () == self.exporter.to_types_view ()
            assert _.to__dot_schema() == self.exporter.to_schema_view()
            assert _.to__dot       () == self.exporter.process_graph()

    def test_node_attribute_formatting(self):                                                       # Test the new node attribute formatting methods
        node_id = self.nodes_ids[0]
        node = self.domain_graph.node(node_id)

        # Test basic attributes
        attrs = self.exporter.create_node_attrs(node)
        assert 'value="A"' in attrs
        assert 'name="Node 1"' in attrs

        # Test with type label
        attrs_with_type = self.exporter.create_node_attrs(node, include_type_label=True)
        assert 'shape=box' in attrs_with_type
        assert 'style="rounded,filled"' in attrs_with_type
        assert 'fillcolor=lightblue' in attrs_with_type
        assert 'label="Schema  Simple  Node"' in attrs_with_type

    def test_edge_line_formatting(self):                                                          # Test the edge line formatting method"""
        edge_1_id = self.edges_ids[0]
        node_1_id = self.nodes_ids[0]
        node_2_id = self.nodes_ids[1]

        # Test without attributes
        edge_data = { 'id'    : str(edge_1_id) ,
                      'source': str(node_1_id)  ,
                      'target': str(node_2_id)  ,
                      'attrs' : []              }
        edge_line = self.exporter.format_edge_line(str(node_1_id), str(node_2_id), edge_data)
        assert f'"{node_1_id}" -> "{node_2_id}"' in edge_line
        assert f'label="  {edge_1_id}"' in edge_line            # Should show edge ID by default

        # Test with show_edge_ids=False
        self.exporter.config.show_edge_ids = False
        edge_line = self.exporter.format_edge_line(str(node_1_id), str(node_2_id), edge_data)
        assert f'"{node_1_id}" -> "{node_2_id}"' in edge_line
        assert '[' not in edge_line                             # No attributes when IDs disabled

        # Test with custom attributes
        edge_data['attrs'] = ['color=blue', 'label="custom"']
        edge_line = self.exporter.format_edge_line(str(node_1_id), str(node_2_id), edge_data)
        assert f'"{node_1_id}" -> "{node_2_id}"' in edge_line
        assert 'color=blue' in edge_line
        assert 'label="custom"' in edge_line

    def test_collect_unique_elements(self):                                                       # Test the collection of unique nodes and edges"""
        unique_nodes, unique_edges = self.exporter.collect_unique_elements()

        # Should only have one node type in our simple graph
        assert len(unique_nodes) == 1
        assert "Schema  Simple  Node" in unique_nodes

        # Should have one edge type between the same node type
        assert len(unique_edges) == 1
        edge_tuple = next(iter(unique_edges))
        assert edge_tuple[0] == "Schema  Simple  Node"  # from_type
        assert edge_tuple[1] == "Schema  Simple  Node"  # to_type
        assert edge_tuple[2] == "Edge"                  # edge_type


    def test_on_add_node(self):                                                             # Test node callback functionality
        def custom_node_handler(node, node_view_data):                                              # Custom node styling based on value
            value = node.node_data.value if node.node_data else None
            if value == "A":
                node_view_data['attrs'] = ['shape=diamond', 'style=filled', 'fillcolor=red'   ]
            if value == "B":
                node_view_data['attrs'] = ['shape=box'    , 'style=filled', 'fillcolor=yellow']

        dot_output = self.exporter.process_graph()                                                                      # first check the result without the custom_node_handler
        assert dot_output == ('digraph {\n'
                              f'  "{self.nodes_ids[0]}" [value="A", name="Node 1"]\n'
                              f'  "{self.nodes_ids[1]}" [value="B", name="Node 2"]\n'
                              f'  "{self.nodes_ids[2]}" [value="C", name="Node 3"]\n'
                              f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[1]}" [label="  {self.edges_ids[0]}"]\n'
                              f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[2]}" [label="  {self.edges_ids[1]}"]\n'
                              '}')

        self.exporter.on_add_node = custom_node_handler                                    # Set the callback
        dot_output                = self.exporter.process_graph()                                                                      # first check the result without the custom_node_handler

        assert dot_output == ('digraph {\n'
                              f'  "{self.nodes_ids[0]}" [shape=diamond, style=filled, fillcolor=red]\n'
                              f'  "{self.nodes_ids[1]}" [shape=box, style=filled, fillcolor=yellow]\n'
                              f'  "{self.nodes_ids[2]}" [value="C", name="Node 3"]\n'
                              f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[1]}" [label="  {self.edges_ids[0]}"]\n'
                              f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[2]}" [label="  {self.edges_ids[1]}"]\n'
                              '}')

    def test_on_add_edge(self):                                                             # Test edge callback functionality
        def custom_edge_handler(edge, from_node, to_node, edge_view_data):                               # Custom edge styling based on connected nodes
            if from_node.node_data.value == "A" and to_node.node_data.value == "B":
                edge_view_data['attrs'] = ['color=blue', 'penwidth=2.0', 'label="A to B"']


        dot_output = self.exporter.process_graph()                                          # first check the result without the custom_node_handler
        assert dot_output == ('digraph {\n'
                              f'  "{self.nodes_ids[0]}" [value="A", name="Node 1"]\n'
                              f'  "{self.nodes_ids[1]}" [value="B", name="Node 2"]\n'
                              f'  "{self.nodes_ids[2]}" [value="C", name="Node 3"]\n'
                              f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[1]}" [label="  {self.edges_ids[0]}"]\n'
                              f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[2]}" [label="  {self.edges_ids[1]}"]\n'
                              '}')

        self.exporter.on_add_edge = custom_edge_handler                                     # Set the callback
        dot_output = self.exporter.process_graph()                                          # get the updated version of the dot code
        assert dot_output == ('digraph {\n'
                              f'  "{self.nodes_ids[0]}" [value="A", name="Node 1"]\n'
                              f'  "{self.nodes_ids[1]}" [value="B", name="Node 2"]\n'
                              f'  "{self.nodes_ids[2]}" [value="C", name="Node 3"]\n'
                              f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[1]}" [label="  {self.edges_ids[0]}", color=blue, penwidth=2.0, label="A to B"]\n'
                              f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[2]}" [label="  {self.edges_ids[1]}"]\n'
                              '}')

    def test_both_callbacks(self):                                                                  # Test both callbacks together
        def node_handler(node, node_view_data):                                                     # Customize nodes with specific values
            if node.node_data and node.node_data.value in ["A", "B"]:
                node_view_data['attrs'] = [f'label="{node.node_data.value}"', 'shape=circle']

        def edge_handler(edge, from_node, to_node, edge_view_data):                                  # Customize edges between specific nodes
            if all(node.node_data for node in [from_node, to_node]):
                edge_view_data['attrs'] =  [f'label="{from_node.node_data.value} -> {to_node.node_data.value}"']

        self.exporter.on_add_node = node_handler                                         # Set both callbacks
        self.exporter.on_add_edge = edge_handler
        self.exporter.process_graph()                                                    # Process the graph
        dot_output = self.exporter.format_output()

        assert dot_output == ('digraph {\n'
                              f'  "{self.nodes_ids[0]}" [label="A", shape=circle]\n'
                              f'  "{self.nodes_ids[1]}" [label="B", shape=circle]\n'
                              f'  "{self.nodes_ids[2]}" [value="C", name="Node 3"]\n'
                              f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[1]}" [label="  {self.edges_ids[0]}", label="A -> B"]\n'
                              f'  "{self.nodes_ids[0]}" -> "{self.nodes_ids[2]}" [label="  {self.edges_ids[1]}", label="A -> C"]\n'
                              '}')
        assert 'label="A"'         in dot_output                                         # Check node customization
        assert 'label="B"'         in dot_output
        assert 'shape=circle'      in dot_output
        assert 'label="A -> B"'    in dot_output                                         # Check edge customization

    # use this to create a screenshot of dot_code
    #
    #         from osbot_utils.utils.Env import load_dotenv
    #         load_dotenv()
    #         self.simple_graph.screenshot().save_to('./export-dot.png').dot_to_png(dot_code)

    #
    #
    # def test__mgraph_screenshot(self):
    #     load_dotenv()
    #     target_file = './dot-file.png'
    #
    #     with self.simple_graph.screenshot(target_file=target_file) as _:
    #         #_.dot__just_values()
    #         #_.dot__just_types()
    #         _.dot_config().show_value    = True
    #         _.dot_config().show_edge_ids = False
    #         _.dot()
    #         assert file_exists(target_file)
    #         assert file_delete(target_file)