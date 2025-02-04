from typing                                                                  import Type
from mgraph_db.mgraph.MGraph                                                 import MGraph
from mgraph_db.providers.time_series.actions.MGraph__Time_Series__Edit       import MGraph__Time_Series__Edit
from mgraph_db.providers.time_series.actions.MGraph__Time_Series__Screenshot import MGraph__Time_Series__Screenshot


class MGraph__Time_Series(MGraph):
    edit_class      : Type[MGraph__Time_Series__Edit      ]
    screenshot_class: Type[MGraph__Time_Series__Screenshot]

    def edit(self) -> MGraph__Time_Series__Edit:                    # todo: figure out if there is a way to provide this type clue without this method (the edit_class      : Type[MGraph__Time_Series__Edit      ] works great, except for the loss of type complete)
        return super().edit()