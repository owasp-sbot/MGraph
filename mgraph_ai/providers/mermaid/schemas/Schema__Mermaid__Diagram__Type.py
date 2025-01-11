from enum import Enum

class Schema__Mermaid__Diagram__Type(Enum):
    class_diagram                = "class_diagram"
    entity_relationship_diagram  = "entity_relationship_diagram"
    flowchart                    = "flowchart"
    gantt                        = "gantt"
    git_graph                    = "git_graph"
    graph                        = "graph"
    mermaid_map                  = "mermaid_map"
    mindmap                      = "mindmap"
    pie_chart                    = "pie_chart"
    requirement_diagram          = "requirement_diagram"
    sequence_diagram             = "sequenceDiagram"             # these are different from the others
    state_diagram                = "stateDiagram-v2"             # these are different from the others
    user_journey                 = "user_journey"