from osbot_utils.type_safe.Type_Safe import Type_Safe

class Model__Cytoscape__Node__Data(Type_Safe):
    id    : str
    type  : str
    label : str

class Model__Cytoscape__Edge__Data(Type_Safe):
    id     : str
    source : str
    target : str
    type   : str

class Model__Cytoscape__Node(Type_Safe):
    data  : Model__Cytoscape__Node__Data

class Model__Cytoscape__Edge(Type_Safe):
    data  : Model__Cytoscape__Edge__Data

class Model__Cytoscape__Elements(Type_Safe):
    nodes : list[Model__Cytoscape__Node]
    edges : list[Model__Cytoscape__Edge]