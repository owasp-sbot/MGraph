from mgraph_ai.domain.MGraph__Attribute import MGraph__Attribute
from mgraph_ai.models.Model__MGraph__Graph import Model__MGraph__Graph
from mgraph_ai.models.Model__MGraph__Node  import Model__MGraph__Node
from osbot_utils.type_safe.Type_Safe       import Type_Safe


class MGraph__Node(Type_Safe):
    node : Model__MGraph__Node
    graph: Model__MGraph__Graph

    def attribute(self, attribute_id):
        attribute = self.node.attributes.get(attribute_id)
        if attribute:
            return MGraph__Attribute(attribute=attribute, graph=self.graph)

    def attributes(self):
        return [MGraph__Attribute(attribute=attribute, graph=self.graph) for attribute in self.node.attributes.values()]