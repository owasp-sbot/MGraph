from mgraph_db.mgraph.actions.MGraph__Data                      import MGraph__Data
from mgraph_db.providers.mermaid.domain.Domain__Mermaid__Graph  import Domain__Mermaid__Graph

class Mermaid__Data(MGraph__Data):
    graph: Domain__Mermaid__Graph

    def nodes__by_key(self):
        by_key = {}
        for node in self.nodes():
            node_key = node.node.data.key               # todo: review this usage and see side effects of type issue mentioned below
            # print()
            # print(node)                                 # BUG: this is MGraph__Node
            # print(node.node)                            # BUG: this is Model__MGraph__Node
            # print(node.node.data)                       # OK : this is Schema__Mermaid__Node
            # print()
            by_key[node_key] = node
        return by_key

    def nodes__keys(self):
        return [node.node.data.key for node in self.nodes()]