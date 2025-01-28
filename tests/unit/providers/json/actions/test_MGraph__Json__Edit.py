from unittest                                                           import TestCase

from osbot_utils.utils.Dev import pprint

from osbot_utils.helpers.Obj_Id                                         import Obj_Id
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node         import Domain__MGraph__Json__Node
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Node__Dict   import Domain__MGraph__Json__Node__Dict
from mgraph_ai.providers.json.models.Model__MGraph__Json__Node__Dict    import Model__MGraph__Json__Node__Dict
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node__Dict  import Schema__MGraph__Json__Node__Dict
from mgraph_ai.providers.json.MGraph__Json                              import MGraph__Json


class test_MGraph__Json__Edit(TestCase):

    def setUp(self):
        self.mgraph_json = MGraph__Json()

    def test_add_root_property_node(self):
        with self.mgraph_json.edit() as _:
            root_property_node = _.add_root_property_node()
            assert type(root_property_node) == Domain__MGraph__Json__Node__Dict

        with self.mgraph_json.export() as _:
            assert _.to_dict() == {}

        with self.mgraph_json.data()  as _:
            assert _.root_property_id() == root_property_node.node_id

            root_property_node =  _.root_property_node()
            assert type(root_property_node          ) == Domain__MGraph__Json__Node                 # this is the generic  Node type        todo: explore the side effects that this is not an object of type Domain__MGraph__Json__Node__Dict
            assert type(root_property_node.node     ) == Model__MGraph__Json__Node__Dict            # this is the specific Node__Dict type
            assert type(root_property_node.node.data) == Schema__MGraph__Json__Node__Dict           # this is the specific Node__Dict type


    def test_add_property(self):
        assert self.mgraph_json.export().to_dict() is None
        with self.mgraph_json.edit() as _:

            root_property_node    = _.add_root_property_node()
            root_property_node_id = root_property_node.node_id
            new_property_1        = _.add_property('abc' , node_id=root_property_node_id             )      # add property with no value
            new_property_2        = _.add_property('1234', node_id=root_property_node_id, value='xyz')      # add property with value
            value_node            = _.add_value  ('12345', node_id=new_property_1.node_id            )      # add value to the property with no value

            assert type(root_property_node   ) is Domain__MGraph__Json__Node__Dict
            assert type(root_property_node_id) is Obj_Id
            assert type(new_property_1       ) is Domain__MGraph__Json__Node
            assert type(new_property_2       ) is Domain__MGraph__Json__Node
            assert type(value_node           ) is Domain__MGraph__Json__Node


        assert self.mgraph_json.export().to_dict() == {'1234': 'xyz', 'abc': '12345'}               # confirm values set correctly

    def test_add_property_to_property(self):
        with self.mgraph_json.edit() as _:
            root_property_node    = _.add_root_property_node()
            new_property_1 = _.add_property('parent', node_id=root_property_node.node_id)
            new_property_2 = _.add_property('child' , node_id=new_property_1.node_id    )

            assert type(new_property_1) == Domain__MGraph__Json__Node
            assert type(new_property_2) == Domain__MGraph__Json__Node
            # print()
            # print('root_property_node', root_property_node.node_id)
            # print('new_property_1    ', new_property_1.node_id    )
            # print('new_property_2    ', new_property_2.node_id    )
            # pprint(new_property_1.node.json())
            pprint(new_property_2.node.json())

        # with self.mgraph_json.index() as _:
        #     _.print()


        #self.mgraph_json.screenshot().save().dot__just_ids()
        #self.mgraph_json.screenshot().save().dot()

        assert self.mgraph_json.export().to_dict() == {'parent': None}   # BUG should be {'parent': { 'child': None }}

        #pprint(self.mgraph_json.export().to_dict())