from typing                                                                      import Optional, Dict, Any
from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node                  import Domain__MGraph__Json__Node
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__Dict             import Model__MGraph__Json__Node__Dict
from mgraph_db.providers.json.models.Model__MGraph__Json__Node__List             import Model__MGraph__Json__Node__List
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Dict           import Schema__MGraph__Json__Node__Dict
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__List           import Schema__MGraph__Json__Node__List
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Property       import Schema__MGraph__Json__Node__Property
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Property__Data import Schema__MGraph__Json__Node__Property__Data
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value          import Schema__MGraph__Json__Node__Value
from mgraph_db.providers.json.schemas.Schema__MGraph__Json__Node__Value__Data    import Schema__MGraph__Json__Node__Value__Data


class Domain__MGraph__Json__Node__Dict(Domain__MGraph__Json__Node):
    node: Model__MGraph__Json__Node__Dict                                                         # Reference to dict node model

    # todo: refactor out these methods which are barely used and have quite a number of performance issues (this will be better done at the MGraph__Json__Data layer
    def properties(self) -> Dict[str, Any]:
        result = {}
        for edge in self.models__from_edges():
            property_node = self.model__node_from_edge(edge)
            property_name = property_node.data.node_data.name
            for value_edge in self.graph.edges():                                           # todo: see why we need to use self.graph.edges()
                if value_edge.from_node_id() == property_node.node_id:
                    value_node = self.graph.node(value_edge.to_node_id())
                    if value_node.data.node_type == Schema__MGraph__Json__Node__Value:              # todo: there is an interest case here, what happens if there is more than one Schema__MGraph__Json__Node__Value per Schema__MGraph__Json__Node__Property
                        result[property_name] = value_node.data.node_data.value                     # todo: solve issue of value not being recognized here
                        break
                    elif value_node.data.node_type == Schema__MGraph__Json__Node__List:
                        from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__List import Domain__MGraph__Json__Node__List
                        list_domain_node = Domain__MGraph__Json__Node__List(node=value_node, graph=self.graph)
                        result[property_name] = list_domain_node.items()
                        break
                    elif value_node.data.node_type == Schema__MGraph__Json__Node__Dict:
                        dict_domain_node = Domain__MGraph__Json__Node__Dict(node=value_node, graph=self.graph)
                        result[property_name] = dict_domain_node.properties()
                        break
                if value_edge.to_node_id() == property_node.node_id:            # when we find the property node_id
                    if result.get('property_name') is None:                     # if it has not been set
                        result[property_name] = None                            # set it to None
        return result

    def property(self, name: str) -> Optional[Any]:                                                                     # Get value of a property by name
        props = self.properties()
        return props.get(name)

    def add_property(self, name: str, value: Any) -> None:                                                              # Add or update a property
        # commented this code to fix performance bug
        # # Find existing property node if any                # BUG
        # for edge in self.models__from_edges():
        #     property_node = self.model__node_from_edge(edge)
        #     if property_node.data.node_type == Schema__MGraph__Json__Node__Property:
        #         if property_node.data.node_data.name == name:
        #             for value_edge in self.graph.node__from_edges(property_node.node_id):
        #
        #                 value_node = self.graph.node(value_edge.to_node_id())
        #                 if value_node.data.node_type is Schema__MGraph__Json__Node__Value:
        #                     value_node.data.node_data.value = value
        #                     return

        # Create new property node and value node

        property_name__schema__node_data = Schema__MGraph__Json__Node__Property__Data(name      = name )
        property_name__schema__node      = Schema__MGraph__Json__Node__Property      (node_data = property_name__schema__node_data)
        property_name__model__node       = self.graph.add_node                       (node      = property_name__schema__node     )
        if type(value) is dict:

            dict_schema_node = Schema__MGraph__Json__Node__Dict()                                               # todo:: find way to use self.model method
            self.graph.data.nodes[dict_schema_node.node_id] = dict_schema_node  # so that we don't need to add this here
            dict_model_node = Model__MGraph__Json__Node__Dict(data=dict_schema_node)
            dict_domain_node = Domain__MGraph__Json__Node__Dict(node=dict_model_node, graph=self.graph)

            dict_domain_node.update(value)

            self.graph.new_edge(from_node_id=self.node_id, to_node_id=property_name__model__node.node_id)
            self.graph.new_edge(from_node_id=property_name__model__node.node_id,to_node_id=dict_schema_node.node_id)
        elif type(value) is list:
            from mgraph_db.providers.json.domain.Domain__MGraph__Json__Node__List import Domain__MGraph__Json__Node__List

            list_schema_node = Schema__MGraph__Json__Node__List()                                               # todo:: find way to use self.model method
            self.graph.data.nodes[list_schema_node.node_id]  = list_schema_node
            list_model_node = Model__MGraph__Json__Node__List(data=list_schema_node)
            list_domain_node = Domain__MGraph__Json__Node__List(node=list_model_node, graph=self.graph)

            list_domain_node.extend(value)

            self.graph.new_edge(from_node_id=self.node_id, to_node_id=property_name__model__node.node_id)
            self.graph.new_edge(from_node_id=property_name__model__node.node_id, to_node_id=list_schema_node.node_id)


        else:
            property_value__schema__node_data = Schema__MGraph__Json__Node__Value__Data  (value     = value, value_type=type(value)      )
            property_value__node_value       = Schema__MGraph__Json__Node__Value         (node_data = property_value__schema__node_data  )
            property_value__model__node      = self.graph.add_node                       (node      = property_value__node_value          )

            self.graph.new_edge(from_node_id=self.node_id                      , to_node_id=property_name__model__node.node_id )
            self.graph.new_edge(from_node_id=property_name__model__node.node_id, to_node_id=property_value__model__node.node_id)

    def update(self, properties: Dict[str, Any]) -> None:                       # Bulk update multiple properties
        for name, value in properties.items():
            self.add_property(name, value)

    def delete_property(self, name: str) -> bool:
        """Remove a property by name"""
        for edge in self.models__from_edges():
            property_node = self.model__node_from_edge(edge)
            if property_node.data.node_type == Schema__MGraph__Json__Node__Property:
                if property_node.data.node_data.name == name:
                    self.graph.delete_edge(edge.edge_id     ())
                    self.graph.delete_node(edge.to_node_id  ())                         # todo: BUG we also need to delete the value node
                    return True
        return False