from mgraph_db.providers.json.actions.MGraph__Json__Data                            import MGraph__Json__Data
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Dict              import Schema__MGraph__Json__Node__Dict
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__List              import Schema__MGraph__Json__Node__List
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Property__Data    import Schema__MGraph__Json__Node__Property__Data
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value             import Schema__MGraph__Json__Node__Value
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value__Data       import Schema__MGraph__Json__Node__Value__Data
from mgraph_db.mgraph.actions.MGraph__Edit                                          import MGraph__Edit
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Property          import Schema__MGraph__Json__Node__Property


class MGraph__Json__Edit(MGraph__Edit):
    data_type : type[MGraph__Json__Data]

    def add_dict(self, node_id=None):                       # todo: add check that node_id is either a property or a list
        node_dict = Schema__MGraph__Json__Node__Dict()
        new_node = self.add_node(node_dict)
        if node_id:
            self.new_edge(from_node_id=node_id, to_node_id= new_node.node_id)
        return new_node

    def add_list(self, node_id=None):                       # todo: add check that node_id is either a property or a list
        node_dict = Schema__MGraph__Json__Node__List()
        new_node = self.add_node(node_dict)
        if node_id:
            self.new_edge(from_node_id=node_id, to_node_id= new_node.node_id)
        return new_node

    def add_property(self, property_name, value=None, node_id=None):
        node_property_data  = Schema__MGraph__Json__Node__Property__Data(name      = property_name     )
        node_property       = Schema__MGraph__Json__Node__Property     (node_data = node_property_data)
        new_node            = self.add_node(node_property)

        if node_id:
            self.new_edge(from_node_id=node_id, to_node_id= new_node.node_id)
            if value:
                self.add_value(value, new_node.node_id)
        return new_node

    def add_root_property_node(self):
        root_property_node = self.root_property_node_id()
        if not root_property_node:
            root_node_id       = self.data().root_node_id()
            root_property_node = self.graph.new_dict_node()
            self.new_edge(from_node_id=root_node_id, to_node_id=root_property_node.node_id)

        return root_property_node

    def add_value(self, value, node_id):
        node_value_data = Schema__MGraph__Json__Node__Value__Data(value     = value     )
        node_value      = Schema__MGraph__Json__Node__Value      (node_data = node_value_data)
        new_node        = self.add_node(node_value)
        if node_id:
            self.new_edge(from_node_id=node_id, to_node_id=new_node.node_id)
        return new_node

    def root_property_node_id(self):
        root_property_id = self.data().root_property_id()
        return root_property_id
