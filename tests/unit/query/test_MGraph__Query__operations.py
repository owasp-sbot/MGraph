import pytest
from unittest                                                import TestCase
from mgraph_db.providers.simple.MGraph__Simple__Test_Data    import MGraph__Simple__Test_Data
from mgraph_db.providers.simple.schemas.Schema__Simple__Node import Schema__Simple__Node


class test_MGraph__Query__operations(TestCase):

    @classmethod
    def setUpClass(cls):
        pytest.skip("Needs fixing after refactoring of MGraph__Index") # todo: for example get_nodes_by_field() doesn't exist any more


    def setUp(self):
        self.mgraph = MGraph__Simple__Test_Data().create()
        self.query  = self.mgraph.query()

    def test_query_chain(self):                                                 # Test query chain with views
        # Initial query
        result1 = self.query.by_type(Schema__Simple__Node)
        view1   = self.query.query_views.current_view()
        assert view1.query_operation() == 'by_type'
        assert len(view1.nodes_ids())  == 3

        # Second query
        result2 = result1.with_field('value', 'A')
        view2   = self.query.query_views.current_view()
        assert view2.query_operation()  == 'with_field'
        assert len(view2.nodes_ids())   == 3
        assert view2.previous_view_id() == view1.view_id()

        # Navigation
        assert self.query.go_back() is True
        current = self.query.query_views.current_view()
        assert current.view_id() == view1.view_id()

        assert self.query.go_forward() is True
        current = self.query.query_views.current_view()
        assert current.view_id() == view2.view_id()

    def test_view_cleanup(self):                                                # Test view cleanup
        view1 = self.query.by_type(Schema__Simple__Node)
        view2 = view1.with_field('value', 'A')
        #view3 = view2.with_field('name', 'Node 1')

        # Remove middle view
        self.query.query_views.remove_view(view2.query_views.current_view().view_id())

        # Navigation should skip removed view
        assert self.query.go_back() is True
        current = self.query.query_views.current_view()
        assert current.view_id() == view1.query_views.current_view().view_id()

    def test_empty_results(self):                                               # Test handling of empty results
        result = self.query.by_type(Schema__Simple__Node).with_field('value', 'NonExistent')
        view   = self.query.query_views.current_view()

        assert result                 == self.query
        assert len(view.nodes_ids ()) == 3                                      # todo: double check these results
        assert len(view.edges_ids ()) == 2
        assert view.query_operation() == 'with_field'
        assert view.query_params   () == {'name': 'value', 'value': 'NonExistent'}