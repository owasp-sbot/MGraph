from unittest                                                           import TestCase
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node         import Domain__MGraph__Json__Node
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__Dict   import Domain__MGraph__Json__Node__Dict

class test__bugs__Domain__MGraph__Json__Node__Dict(TestCase):                     # Test that captures the property visibility bug

    def setUp(self):                                                            # Prepare test environment with a domain dictionary
        self.domain_graph     = Domain__MGraph__Json__Node()
        self.domain_node_dict = Domain__MGraph__Json__Node__Dict(graph=self.domain_graph.graph)
        self.domain_graph.add_node(self.domain_node_dict.node)

    def test_bug__deleted_property_still_visible(self):                         # Test passes while bug exists, will fail when fixed
        with self.domain_node_dict as _:
            _.add_property("key", "initial")                                    # Add initial property to create baseline state
            assert _.properties()    == {"key": "initial"}                      # Verify property was correctly added

            _.add_property("key", "updated")                                    # Update existing property with new value
            assert _.delete_property("key") is True                             # Delete property once - should remove it completely
            assert _.property("key")        == 'updated'
            assert _.properties()           == {"key": "updated"}               # BUG: Property still visible after deletion

            assert _.delete_property("key") is True                             # BUG: Need second delete due to multiple instances
            assert _.delete_property("key") is False                            # Third delete fails as all instances are gone
            assert _.properties() == {}                                         # Dictionary finally shows as empty

            assert len(_.graph.nodes_ids()) == 3                                # BUG: Have 3 orphaned nodes that weren't cleaned up
            assert len(_.graph.edges_ids()) == 0                                # Edge cleanup works correctly
            assert self.domain_node_dict.node_id in _.graph.nodes_ids()         # Original dictionary node still present