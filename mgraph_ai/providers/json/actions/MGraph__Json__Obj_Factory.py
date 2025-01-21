from mgraph_ai.mgraph.schemas.Schema__MGraph__Node__Data            import Schema__MGraph__Node__Data
from mgraph_ai.providers.json.schemas.Schema__MGraph__Json__Node    import Schema__MGraph__Json__Node
from osbot_utils.helpers.Obj_Id                                     import Obj_Id
from osbot_utils.type_safe.Type_Safe                                import Type_Safe


class MGraph__Json__Obj_Factory(Type_Safe):

    def create__Schema__MGraph__Node__Data(self):
        return object.__new__(Schema__MGraph__Node__Data)

    def create__Schema__MGraph__Json__Node(self):
        node_data        = self.create__Schema__MGraph__Node__Data()
        schema_node      = object.__new__(Schema__MGraph__Json__Node)
        schema_node_dict = dict(node_data = node_data                 ,
                                node_id   = Obj_Id()                  ,
                                node_type = Schema__MGraph__Json__Node)
        object.__setattr__(schema_node, '__dict__', schema_node_dict)

        return schema_node


