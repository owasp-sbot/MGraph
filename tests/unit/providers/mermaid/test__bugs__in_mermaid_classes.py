from unittest                                                            import TestCase
from mgraph_ai.mgraph.schemas.Schema__MGraph__Default__Types             import Schema__MGraph__Default__Types
from mgraph_ai.providers.mermaid.domain.Mermaid__Node                    import Mermaid__Node
from mgraph_ai.providers.mermaid.models.Model__Mermaid__Graph            import Model__Mermaid__Graph
from mgraph_ai.providers.mermaid.models.Model__Mermaid__Node             import Model__Mermaid__Node
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Default__Types import Schema__Mermaid__Default__Types
from mgraph_ai.providers.mermaid.schemas.Schema__Mermaid__Graph          import Schema__Mermaid__Graph


class test__bug__in_mermaid_classes(TestCase):

    def test__bug__json_roundtrip(self):
        # these will fail if
        #   attribute_type   : Type[Schema__MGraph__Attribute]
        # is not in Schema__Mermaid__Default__Types
        # with pytest.raises(ValueError, match=re.escape("Invalid type for attribute 'attribute_type'. Expected 'typing.Type[mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute.Schema__MGraph__Attribute]' but got '<class 'str'>'")):
        #     Mermaid__Node.from_json(Mermaid__Node().json())
        # with pytest.raises(ValueError, match=re.escape("Invalid type for attribute 'attribute_type'. Expected 'typing.Type[mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute.Schema__MGraph__Attribute]' but got '<class 'str'>'")):
        #     Model__Mermaid__Graph.from_json(Model__Mermaid__Graph().json())
        # with pytest.raises(ValueError, match=re.escape("Invalid type for attribute 'attribute_type'. Expected 'typing.Type[mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute.Schema__MGraph__Attribute]' but got '<class 'str'>'")):
        #     Schema__Mermaid__Graph.from_json(Schema__Mermaid__Graph().json())
        # with pytest.raises(ValueError, match=re.escape("Invalid type for attribute 'attribute_type'. Expected 'typing.Type[mgraph_ai.mgraph.schemas.Schema__MGraph__Attribute.Schema__MGraph__Attribute]' but got '<class 'str'>'")):
        #     Schema__Mermaid__Default__Types.from_json(Schema__Mermaid__Default__Types().json())

        # these only work with the attribute in there
        mermaid_node = Mermaid__Node()
        assert Mermaid__Node.from_json(mermaid_node.json()).json() == mermaid_node.json()
        Mermaid__Node                  .from_json(Mermaid__Node                  ().json())
        Model__Mermaid__Graph          .from_json(Model__Mermaid__Graph          ().json())
        Schema__Mermaid__Graph         .from_json(Schema__Mermaid__Graph         ().json())
        Schema__Mermaid__Default__Types.from_json(Schema__Mermaid__Default__Types().json())

        # these work without the attribute in there
        Schema__MGraph__Default__Types.from_json(Schema__MGraph__Default__Types().json())
        Model__Mermaid__Node.from_json(Model__Mermaid__Node().json())
