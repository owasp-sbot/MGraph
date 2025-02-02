from mgraph_db.mgraph.schemas.Schema__MGraph__Graph__Data import Schema__MGraph__Graph__Data

class Schema__Mermaid__Graph__Config(Schema__MGraph__Graph__Data):
    allow_circle_edges    : bool
    allow_duplicate_edges : bool
    graph_title           : str