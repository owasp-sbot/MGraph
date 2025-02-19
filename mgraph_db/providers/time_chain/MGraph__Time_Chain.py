from mgraph_db.mgraph.MGraph import MGraph
from mgraph_db.providers.time_chain.actions.MGraph__Time_Chain__Create import MGraph__Time_Chain__Create


class MGraph__Time_Chain(MGraph):

    def create(self):
        mgraph_edit = self.edit()
        return MGraph__Time_Chain__Create(mgraph_edit=mgraph_edit)