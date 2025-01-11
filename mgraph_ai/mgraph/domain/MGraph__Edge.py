from typing                                                import Any, List
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config import Schema__MGraph__Edge__Config
from osbot_utils.helpers.Random_Guid                       import Random_Guid
from osbot_utils.helpers.Safe_Id                           import Safe_Id
from mgraph_ai.mgraph.domain.MGraph__Node                  import MGraph__Node
from mgraph_ai.mgraph.models.Model__MGraph__Attribute      import Model__MGraph__Attribute
from mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute    import Schema__MGraph__Attribute
from mgraph_ai.mgraph.domain.MGraph__Attribute             import MGraph__Attribute
from mgraph_ai.mgraph.models.Model__MGraph__Edge           import Model__MGraph__Edge
from mgraph_ai.mgraph.models.Model__MGraph__Graph          import Model__MGraph__Graph
from osbot_utils.type_safe.Type_Safe                       import Type_Safe

class MGraph__Edge(Type_Safe):                                                              # Domain class for edges
    edge : Model__MGraph__Edge                                                              # Reference to edge model
    graph: Model__MGraph__Graph                                                             # Reference to graph model

    def config(self) -> Schema__MGraph__Edge__Config:
        return self.edge.data.edge_config

    def edge_id(self) -> Random_Guid:                                                            # Get edge ID
        return self.edge.data.edge_config.edge_id

    def from_node(self) -> MGraph__Node:                                                    # Get source node
        node = self.graph.node(self.edge.from_node_id())
        if node:
            return MGraph__Node(node=node, graph=self.graph )

    def to_node(self) -> MGraph__Node:                                                      # Get target node
        node = self.graph.node(self.edge.to_node_id())
        if node:
            return MGraph__Node(node=node, graph=self.graph)

    def add_attribute(self, name     : Safe_Id    ,
                            value    : Any        ,                                          # Add a new attribute to edge
                            attr_type: type = None) -> 'MGraph__Edge':

        attribute = Schema__MGraph__Attribute(attribute_id   = Random_Guid()            ,
                                              attribute_name  = name                    ,
                                              attribute_value = value                   ,
                                              attribute_type  = attr_type or type(value))
        self.edge.add_attribute(attribute)
        return self

    def attribute(self, attribute_id: Random_Guid) -> MGraph__Attribute:                    # Get an attribute by ID
        data = self.edge.get_attribute(attribute_id)
        if data:
            return  MGraph__Attribute(attribute = Model__MGraph__Attribute(data=data),
                                      graph     = self.graph                         )

    def attributes(self) -> List[MGraph__Attribute]:                                       # Get all edge attributes
        return [MGraph__Attribute(attribute = Model__MGraph__Attribute(data=attr),
                                  graph     = self.graph                         )
                for attr in self.edge.data.attributes.values()]