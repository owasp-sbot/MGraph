from osbot_utils.type_safe.Type_Safe import Type_Safe


class Schema__Graph_RAG__Direct_Relationship(Type_Safe):
    entity            : str                                 # Related entity name
    relationship_type : str                                 # Type of relationship
    strength          : float = 1.0                         # Relationship strength (0-1)