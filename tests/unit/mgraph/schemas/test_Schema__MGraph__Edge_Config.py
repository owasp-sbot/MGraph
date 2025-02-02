from unittest                                               import TestCase
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge__Config  import Schema__MGraph__Edge__Config
from mgraph_db.mgraph.schemas.Schema__MGraph__Node          import Schema__MGraph__Node
from osbot_utils.helpers.Obj_Id                             import Obj_Id

class Simple_Node(Schema__MGraph__Node): pass    # Helper class for testing

class test_Schema__MGraph__Edge__Config(TestCase):

    def setUp(self):    # Initialize test data
        self.edge_id        = Obj_Id()
        self.edge_config    = Schema__MGraph__Edge__Config(edge_id        = self.edge_id)

    def test_init(self):    # Tests basic initialization and type checking
        assert type(self.edge_config) is Schema__MGraph__Edge__Config
        assert self.edge_config.edge_id == self.edge_id

    def test_type_safety_validation(self):    # Tests type safety validations
        with self.assertRaises(ValueError) as context:
            Schema__MGraph__Edge__Config(edge_id="not-a-guid")
        assert str(context.exception) == "in Obj_Id: value provided was not a valid Obj_Id: not-a-guid"