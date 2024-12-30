from mgraph_ai.core.MGraph__Data import MGraph__Data


class Mermaid__Data(MGraph__Data):
    def nodes__by_key(self):
        by_key = {}
        for node in self.nodes():
            by_key[node.key] = node
        return by_key

    def nodes__keys(self):
        return [node.key for node in self.nodes()]