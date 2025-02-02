from unittest                                               import TestCase
from mgraph_db.mgraph.actions.MGraph__Export                import MGraph__Export
from mgraph_db.mgraph.actions.exporters.MGraph__Export__Dot import MGraph__Export__Dot, MGraph__Export__Dot__Config
from mgraph_db.mgraph.domain.Domain__MGraph__Graph          import Domain__MGraph__Graph
from mgraph_db.mgraph.models.Model__MGraph__Graph           import Model__MGraph__Graph
from mgraph_db.mgraph.schemas.Schema__MGraph__Graph         import Schema__MGraph__Graph
from mgraph_db.providers.simple.MGraph__Simple__Test_Data   import MGraph__Simple__Test_Data

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
                          '  "Schema  Simple  Node" [shape=box, style="rounded,filled", fillcolor=lightblue, value="A", name="Node 1"]\n'
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
        with MGraph__Export(graph=self.domain_graph) as _:
            assert _.to__dot_types () == self.exporter.to_types_view ()
            assert _.to__dot_schema() == self.exporter.to_schema_view()
