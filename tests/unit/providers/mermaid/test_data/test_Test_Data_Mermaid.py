from unittest                                                   import TestCase
from mgraph_ai.providers.mermaid.test_data.Test_Data__Mermaid   import Test_Data_Mermaid
from osbot_utils.helpers.Safe_Id                                import Safe_Id
from mgraph_ai.providers.mermaid.models.Model__Mermaid__Graph   import Model__Mermaid__Graph
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Graph import Schema__Mermaid__Graph

class test_Test_Data_Mermaid(TestCase):

    def test_create_test_graph(self):                                                       # Test with default number of nodes
        data = Test_Data_Mermaid.create_test_graph()

        # Verify structure
        assert 'graph' in data
        assert 'graph_model' in data
        assert 'graph_data' in data
        assert 'graph_config' in data
        assert 'nodes' in data
        assert 'node_keys' in data

        # Verify types
        assert isinstance(data['graph_data'], Schema__Mermaid__Graph)
        assert isinstance(data['graph_model'], Model__Mermaid__Graph)
        assert len(data['nodes']) == 3  # Default number of nodes
        assert len(data['node_keys']) == 3

        # Verify node keys format
        for key in data['node_keys']:
            assert isinstance(key, Safe_Id)
            assert key.startswith('key_')

        # Test with custom number of nodes
        data_custom = Test_Data_Mermaid.create_test_graph(num_nodes=5)
        assert len(data_custom['nodes']) == 5
        assert len(data_custom['node_keys']) == 5

    def test_create_empty_graph(self):
        data = Test_Data_Mermaid.create_empty_graph()

        # Verify structure
        assert 'graph' in data
        assert 'graph_model' in data
        assert 'graph_data' in data
        assert 'graph_config' in data

        # Verify empty state
        assert len(data['graph_data'].nodes) == 0
        assert len(data['graph_data'].edges) == 0
        assert isinstance(data['graph_data'], Schema__Mermaid__Graph)
        assert isinstance(data['graph_model'], Model__Mermaid__Graph)
        assert data['graph_data'].mermaid_code == []