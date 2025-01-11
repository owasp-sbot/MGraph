import pytest
from unittest                                                                   import TestCase
from osbot_utils.helpers.Random_Guid                                            import Random_Guid
from mgraph_ai.providers.file_system.schemas.Schema__File_System__Graph__Config import Schema__File_System__Graph__Config


class test_Schema__File_System__Graph__Config(TestCase):

    def setUp(self):                                                                              # Initialize test data
        self.graph_id           = Random_Guid()
        self.allow_circular_refs = False
        self.graph_config       = Schema__File_System__Graph__Config(
                                    graph_id           = self.graph_id,
                                    allow_circular_refs = self.allow_circular_refs)

    def test_init(self):                                                                         # Tests basic initialization and type checking
        assert type(self.graph_config)                is Schema__File_System__Graph__Config
        assert self.graph_config.graph_id             == self.graph_id
        assert self.graph_config.allow_circular_refs  == self.allow_circular_refs

    def test_type_safety_validation(self):                                                       # Tests type safety validations
        with pytest.raises(ValueError, match="Invalid type for attribute 'graph_id'. Expected '<class 'osbot_utils.helpers.Random_Guid.Random_Guid'>' but got '<class 'str'>'"):
                Schema__File_System__Graph__Config(graph_id           = "not-a-guid",                                               # Should be Random_Guid
                                                   allow_circular_refs = self.allow_circular_refs)

        with pytest.raises(ValueError, match="Invalid type for attribute 'allow_circular_refs'. Expected '<class 'bool'>' but got '<class 'str'>'"):
            Schema__File_System__Graph__Config(graph_id           = self.graph_id,
                                               allow_circular_refs = "not-a-bool")                                                  # Should be bool


