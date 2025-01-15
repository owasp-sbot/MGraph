from mgraph_ai.mgraph.domain.Domain__MGraph__Graph               import Domain__MGraph__Graph
from mgraph_ai.providers.json.domain.Domain__MGraph__Json__Types import Domain__MGraph__Json__Types
from mgraph_ai.providers.json.models.Model__MGraph__Json__Graph  import Model__MGraph__Json__Graph


class Domain__MGraph__Json__Graph(Domain__MGraph__Graph):
    domain_types : Domain__MGraph__Json__Types
    model        : Model__MGraph__Json__Graph