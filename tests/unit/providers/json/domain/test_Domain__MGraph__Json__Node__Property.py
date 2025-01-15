from unittest import TestCase

import pytest


class test_Domain__MGraph__Json__Node__Property(TestCase):

    def setUp(self):
        pytest.skip("todo: fix test")# Initialize test data


    def test_property_name(self):                                                        # Test property name handling
        property_name = "test_property"
        node = self.graph.new_node(name=property_name)

        assert isinstance(node, Domain__MGraph__Json__Node__Property)
        assert node.name == property_name