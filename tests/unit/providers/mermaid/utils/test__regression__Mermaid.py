from unittest                                                   import TestCase
from mgraph_ai.providers.mermaid.domain.Domain__Mermaid__Edge   import Domain__Mermaid__Edge
from mgraph_ai.providers.mermaid.domain.Domain__Mermaid__Graph  import Domain__Mermaid__Graph
from mgraph_ai.providers.mermaid.domain.Domain__Mermaid__Node   import Domain__Mermaid__Node
from mgraph_ai.providers.mermaid.models.Model__Mermaid__Edge    import Model__Mermaid__Edge
from mgraph_ai.providers.mermaid.models.Model__Mermaid__Node    import Model__Mermaid__Node
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge  import Schema__Mermaid__Edge
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node  import Schema__Mermaid__Node
from mgraph_ai.providers.mermaid.utils.Mermaid__Random_Graph    import create_test_mermaid_graph


class test__regression__Mermaid(TestCase):

    def test__regression__domain_node_type_mismatch(self):                     # Bug: Domain node type should be Mermaid__Node but is MGraph__Node
        with create_test_mermaid_graph() as graph:
            domain_node = graph.graph.nodes()[0]

            # Current incorrect behavior
            # assert type(domain_node)      is MGraph__Node        # ✗ Wrong
            # assert type(domain_node.node) is Model__MGraph__Node # ✗ Wrong

            #Expected behavior (currently fails)
            assert type(domain_node) is Domain__Mermaid__Node          # ✓ Should be this
            assert type(domain_node.node) is Model__Mermaid__Node   # ✓ Should be this

    def test__regression__model_node_type_mismatch(self):                      # Bug: Model node type should be Model__Mermaid__Node but is Model__MGraph__Node
        with create_test_mermaid_graph() as graph:
            model_node = graph.graph.model.nodes()[0]

            # Current incorrect behavior
            # assert type(model_node)      is Model__MGraph__Node  # ✗ Wrong
            # assert type(model_node.data) is Schema__Mermaid__Node

            #Expected behavior (currently fails)
            assert type(model_node)      is Model__Mermaid__Node # ✓ Should be this

    def test__regression__domain_edge_type_mismatch(self):  # Bug: Domain edge type should be Mermaid__Edge but is MGraph__Edge
        with create_test_mermaid_graph() as graph:
            domain_edge = graph.graph.edges()[0]

            # Current incorrect behavior (Fixed)
            # assert type(domain_edge)                is MGraph__Edge           # Fixed: ✗ Wrong
            # assert type(domain_edge.edge)           is Model__MGraph__Edge    # Fixed:  ✗ Wrong

            # Expected behavior (Fixed)
            assert type(domain_edge)                               is Domain__Mermaid__Edge   # Fixed:  ✓ Should be this
            assert type(domain_edge.edge)                          is Model__Mermaid__Edge    # Fixed:  ✓ Should be this
            assert domain_edge.graph.default_types.edge_model_type == Model__Mermaid__Edge    # Fixed:  ✓ Should be this

    def test__regression__model_edge_type_mismatch(self):                                        # Bug: Model edge type should be Model__Mermaid__Edge but is Model__MGraph__Edge
        with create_test_mermaid_graph() as graph:
            model_edge = graph.graph.model.edges()[0]
            assert type(model_edge     ) is Model__Mermaid__Edge             # ✓ Correct
            assert type(model_edge.data) is Schema__Mermaid__Edge

    def test__regression__direct_node_type_mismatch(self):
        graph        = Domain__Mermaid__Graph()
        graph_model  = graph.model
        mermaid_node = Schema__Mermaid__Node()
        model_node   = graph_model.add_node(mermaid_node)
        node_id      = model_node.node_id
        domain_node  = graph.node(model_node.node_id)                     # Get node through domain layer

        assert graph_model.default_types.node_model_type  == Model__Mermaid__Node       # ✓ Correct
        assert graph_model.default_types.edge_model_type  == Model__Mermaid__Edge       # ✓ Correct
        assert type(model_node)                           is Model__Mermaid__Node
        assert isinstance(model_node     , Model__Mermaid__Node )                       # ✓ Correct
        assert isinstance(model_node.data, Schema__Mermaid__Node)                       # ✓ Correct
        assert type(graph.model.nodes()[0])               == Model__Mermaid__Node       # ✓ Correct
        assert type(graph.model.data.nodes[node_id])      == Schema__Mermaid__Node      # ✓ Correct
        assert type(domain_node     )                     == Domain__Mermaid__Node      # ✓ Correct
        assert type(graph.nodes()[0])                     == Domain__Mermaid__Node      # ✓ Correct