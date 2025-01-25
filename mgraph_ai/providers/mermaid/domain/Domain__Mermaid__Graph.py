from mgraph_ai.mgraph.domain.Domain__MGraph__Graph             import Domain__MGraph__Graph
from mgraph_ai.providers.mermaid.domain.Domain__Mermaid__Types import Domain__Mermaid__Types
from mgraph_ai.providers.mermaid.models.Model__Mermaid__Graph  import Model__Mermaid__Graph

class Domain__Mermaid__Graph(Domain__MGraph__Graph):
    domain_types: Domain__Mermaid__Types
    model        : Model__Mermaid__Graph
