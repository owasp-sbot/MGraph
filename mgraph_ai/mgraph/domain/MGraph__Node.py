from typing                                             import Any, List
from osbot_utils.helpers.Random_Guid                    import Random_Guid
from osbot_utils.helpers.Safe_Id                        import Safe_Id
from mgraph_ai.mgraph.models.Model__MGraph__Attribute   import Model__MGraph__Attribute
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute import Schema__MGraph__Attribute
from mgraph_ai.mgraph.domain.MGraph__Attribute          import MGraph__Attribute
from mgraph_ai.mgraph.models.Model__MGraph__Graph       import Model__MGraph__Graph
from mgraph_ai.mgraph.models.Model__MGraph__Node        import Model__MGraph__Node
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

class MGraph__Node(Type_Safe):                                                             # Domain class for nodes
    node : Model__MGraph__Node                                                             # Reference to node model
    graph: Model__MGraph__Graph                                                            # Reference to graph model

    def node_config(self):
        return self.node.data.node_config

    def node_id(self) -> Random_Guid:
        return self.node.data.node_config.node_id

    def value(self) -> Any:                                                                # Get node value
        return self.node.value()

    def set_value(self, value: Any) -> 'MGraph__Node':                                    # Set node value with type checking
        self.node.set_value(value)
        return self

    def add_attribute(self, name     : Safe_Id    ,
                            value    : Any        ,
                            attr_type: type = None) -> 'MGraph__Node':                      # Add a new attribute to node

        attribute = Schema__MGraph__Attribute(attribute_id    = Random_Guid()           ,
                                              attribute_name  = name                    ,
                                              attribute_value = value                   ,
                                              attribute_type  = attr_type or type(value))
        self.node.add_attribute(attribute)
        return self

    def attribute(self, attribute_id: Random_Guid) -> MGraph__Attribute:                    # Get an attribute by ID
        data = self.node.attribute(attribute_id)
        if data:
            return MGraph__Attribute(attribute = Model__MGraph__Attribute(data=data),
                                     graph     = self.graph                         )

    def attributes(self) -> List[MGraph__Attribute]:                                       # Get all node attributes
        return [MGraph__Attribute(attribute = Model__MGraph__Attribute(data=attr),
                                  graph     = self.graph                         )
                for attr in self.node.data.attributes.values()]

    def graph_id(self):
        return self.graph.data.graph_config.graph_id