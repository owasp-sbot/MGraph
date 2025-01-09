from unittest                                                   import TestCase
from mgraph_ai.providers.mermaid.domain.Mermaid__Graph          import Mermaid__Graph
from mgraph_ai.mgraph.domain.MGraph__Edge                       import MGraph__Edge
from mgraph_ai.mgraph.domain.MGraph__Node                       import MGraph__Node
from mgraph_ai.mgraph.models.Model__MGraph__Edge                import Model__MGraph__Edge
from mgraph_ai.mgraph.models.Model__MGraph__Node                import Model__MGraph__Node
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge  import Schema__Mermaid__Edge
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Node  import Schema__Mermaid__Node
from mgraph_ai.providers.mermaid.utils.Mermaid__Random_Graph    import create_test_mermaid_graph


class test__bugs__Mermaid(TestCase):

    def test_bug_domain_node_type_mismatch(self):                     # Bug: Domain node type should be Mermaid__Node but is MGraph__Node
        with create_test_mermaid_graph() as graph:
            domain_node = graph.graph.nodes()[0]

            # Current incorrect behavior
            assert type(domain_node)      is MGraph__Node        # ✗ Wrong
            assert type(domain_node.node) is Model__MGraph__Node # ✗ Wrong

            # Expected behavior (currently fails)
            # assert type(domain_node)      is Mermaid__Node     # ✓ Should be this
            # assert type(domain_node.node) is Model__Mermaid__Node # ✓ Should be this

    def test_bug_model_node_type_mismatch(self):                      # Bug: Model node type should be Model__Mermaid__Node but is Model__MGraph__Node
        with create_test_mermaid_graph() as graph:
            model_node = graph.graph.model.nodes()[0]

            # Current incorrect behavior
            assert type(model_node)      is Model__MGraph__Node  # ✗ Wrong
            assert type(model_node.data) is Schema__Mermaid__Node

            # Expected behavior (currently fails)
            # assert type(model_node)      is Model__Mermaid__Node # ✓ Should be this

    def test_bug_domain_edge_type_mismatch(self):  # Bug: Domain edge type should be Mermaid__Edge but is MGraph__Edge
        with create_test_mermaid_graph() as graph:
            domain_edge = graph.graph.edges()[0]

            # Current incorrect behavior
            assert type(domain_edge)                is MGraph__Edge  # ✗ Wrong
            assert type(domain_edge.edge)           is Model__MGraph__Edge  # ✗ Wrong

            # Expected behavior (currently fails)
            # assert type(domain_edge)      is Mermaid__Edge     # ✓ Should be this
            # assert type(domain_edge.edge) is Model__Mermaid__Edge # ✓ Should be this
            # assert domain_edge.graph.edge_model_type == Model__Mermaid__Edge # ✓ Should be this

    def test_bug_model_edge_type_mismatch(
            self):  # Bug: Model edge type should be Model__Mermaid__Edge but is Model__MGraph__Edge
        with create_test_mermaid_graph() as graph:
            model_edge = graph.graph.model.edges()[0]

            # Current incorrect behavior
            assert type(model_edge) is Model__MGraph__Edge  # ✗ Wrong
            assert type(model_edge.data) is Schema__Mermaid__Edge

            # Expected behavior (currently fails)
            # assert type(model_edge)      is Model__Mermaid__Edge # ✓ Should be this

    def test_direct_node_type_mismatch(self):
        graph        = Mermaid__Graph()
        graph_model  = graph.model
        mermaid_node = Schema__Mermaid__Node()
        model_node   = graph_model.add_node(mermaid_node)

        # Current behavior (showing type mismatch)
        assert isinstance(model_node     , Model__MGraph__Node  )  # ✗ Wrong: Should be Model__Mermaid__Node
        assert isinstance(model_node.data, Schema__Mermaid__Node)  # ✓ Correct


        domain_node = graph.node(mermaid_node.node_config.node_id)              # Get node through domain layer
        assert isinstance(domain_node, MGraph__Node)                            # ✗ Wrong: Should be Mermaid__Node