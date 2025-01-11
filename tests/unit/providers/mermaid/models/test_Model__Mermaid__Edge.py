from unittest                                                           import TestCase
from mgraph_ai.mgraph.models.Model__MGraph__Edge                        import Model__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge                      import Schema__MGraph__Edge
from mgraph_ai.mgraph.schemas.Schema__MGraph__Edge__Config              import Schema__MGraph__Edge__Config
from osbot_utils.helpers.Random_Guid                                    import Random_Guid
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge          import Schema__Mermaid__Edge
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Edge__Config  import Schema__Mermaid__Edge__Config
from mgraph_ai.providers.mermaid.models.Model__Mermaid__Edge            import Model__Mermaid__Edge

class test_Model__Mermaid__Edge(TestCase):

    def setUp(self):                                                                        # Initialize test data
        self.from_node_id = Random_Guid()
        self.to_node_id   = Random_Guid()
        self.edge_config  = Schema__Mermaid__Edge__Config(edge_id        = Random_Guid()          )
        self.edge         = Schema__Mermaid__Edge        (attributes     = {}                     ,
                                                          edge_config    = self.edge_config       ,
                                                          edge_type      = Schema__Mermaid__Edge  ,
                                                          from_node_id   = self.from_node_id      ,
                                                          to_node_id     = self.to_node_id        ,
                                                          label          = "Test Label"           )
        self.model        = Model__Mermaid__Edge         (data           = self.edge              )

    def test_init(self):                                                                    # Tests basic initialization
        assert type(self.model)          is Model__Mermaid__Edge
        assert self.model.data           is self.edge
        assert self.model.from_node_id() == self.from_node_id
        assert self.model.to_node_id()   == self.to_node_id
        assert self.model.data.label     == "Test Label"

    def test_inheritance_from_model_mgraph_edge(self):                                      # Tests inheritance behavior
        assert isinstance(self.model, Model__MGraph__Edge)                                  # Verify that Model__Mermaid__Edge inherits Model__MGraph__Edge
        assert self.model.edge_id() == self.edge_config.edge_id                            # Test inherited methods

        # Test edge config retrieval
        retrieved_config = self.model.edge_config()
        assert retrieved_config == self.edge_config
        assert isinstance(retrieved_config, Schema__Mermaid__Edge__Config)

    def test_mermaid_specific_implementations(self):                                        # Tests Mermaid-specific implementations
        assert issubclass(Schema__Mermaid__Edge, Schema__MGraph__Edge)                     # Verify schema inheritance
        assert hasattr(Schema__Mermaid__Edge(), 'label')

        assert isinstance(self.edge_config, Schema__Mermaid__Edge__Config)                 # Verify that the edge uses Mermaid-specific config
        assert issubclass(Schema__Mermaid__Edge__Config, Schema__MGraph__Edge__Config)

        assert issubclass(Model__Mermaid__Edge, Model__MGraph__Edge)    is True           # Verify model inheritance
        assert isinstance(self.model.data, Schema__Mermaid__Edge)       is True
        assert type(self.model.data)                                    is Schema__Mermaid__Edge
        assert not type(self.model.data)                                is Schema__MGraph__Edge