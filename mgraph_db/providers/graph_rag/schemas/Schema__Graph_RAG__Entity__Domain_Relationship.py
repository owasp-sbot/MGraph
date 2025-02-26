from osbot_utils.type_safe.Type_Safe import Type_Safe


class Schema__Graph_RAG__Entity__Domain_Relationship(Type_Safe):
    concept           : str                                   # Domain concept
    relationship_type : str                                   # Type of relationship
    category          : str                                   # Category of the concept
    strength          : float                                 # Relationship strength (0-1)

