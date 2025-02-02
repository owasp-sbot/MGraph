from typing                                                                     import Dict, List, Any
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Document__Data    import Schema__Graph_RAG__Document__Data
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Relation__Data    import Schema__Graph_RAG__Relation__Data
from mgraph_db.providers.graph_rag.testing.MGraph__Graph_Rag__LLM_Cache__Simple import mgraph_llm_cache_simple
from mgraph_db.providers.llms.utils.API__LLM                                    import API__LLM
from osbot_utils.helpers.Obj_Id                                                 import Obj_Id
from osbot_utils.helpers.xml.rss.RSS__Item                                      import RSS__Item
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Entity            import Schema__Graph_RAG__Entity
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Entity__Data      import Schema__Graph_RAG__Entity__Data
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Relation          import Schema__Graph_RAG__Relation
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Document          import Schema__Graph_RAG__Document


class Graph_RAG__Document__Processor(Type_Safe):
    api_llm : API__LLM                                                          # Reference to LLM API client

    def process_rss_item(self, item: RSS__Item) -> Schema__Graph_RAG__Document:
        document_data = Schema__Graph_RAG__Document__Data(title      = item.title       ,
                                                          content    = item.description ,
                                                          pub_date   = item.pubDate     ,
                                                          source_url = item.link        ,
                                                          metadata   = { 'guid'      : item.guid      ,
                                                                         'categories': item.categories,
                                                                         'creator'   : item.creator   })
        return Schema__Graph_RAG__Document(
            node_data=document_data,
            node_id=Obj_Id(),
            node_type=Schema__Graph_RAG__Document
        )                                                                       # Convert RSS item to document node

    def create_entities_prompt(self, text: str) -> Dict[str, Any]:               # Create structured prompt for entity extraction
        target_model = "gpt-4o-mini"

        content_prompt = """You are a comprehensive knowledge extractor that maps entities into a rich semantic network.
                           For each entity:
                           1. Identify its core essence and domain classifications
                           2. Map its functional roles (keep these brief and specific)
                           3. Identify its technical ecosystem and standards
                           4. Map both direct relationships (from the text) and broader knowledge relationships
                           Be specific and precise. Avoid descriptions - focus on relationships and classifications.
                           Return only valid JSON with no additional text."""

        items = {"type": "object",
                 "properties": {
                     "name": {
                         "type": "string",
                         "description": "Core entity name"
                     },
                     "primary_domains": {
                         "type": "array",
                         "items": {"type": "string"},
                         "description": "Main domains this entity belongs to (e.g., Security, Development, Infrastructure)"
                     },
                     "functional_roles": {
                         "type": "array",
                         "items": {"type": "string"},
                         "description": "Specific functions/purposes (e.g., Framework, Protocol, Standard, Tool)"
                     },
                     "ecosystem": {
                         "type": "object",
                         "properties": {
                             "platform": {"type": "string"},
                             "standards": {
                                 "type": "array",
                                 "items": {"type": "string"}
                             },
                             "technologies": {
                                 "type": "array",
                                 "items": {"type": "string"}
                             }
                         },
                         "description": "Technical context and related standards/technologies"
                     },
                     "direct_relationships": {
                         "type": "array",
                         "items": {
                             "type": "object",
                             "properties": {
                                 "entity": {"type": "string"},
                                 "relationship_type": {"type": "string"},
                                 "strength": {"type": "number", "minimum": 0, "maximum": 1}
                             }
                         },
                         "description": "Relationships with other entities found in the text"
                     },
                     "domain_relationships": {
                         "type": "array",
                         "items": {
                             "type": "object",
                             "properties": {
                                 "concept": {"type": "string"},
                                 "relationship_type": {"type": "string"},
                                 "category": {"type": "string"},
                                 "strength": {"type": "number", "minimum": 0, "maximum": 1}
                             }
                         },
                         "description": "Related concepts from the broader domain knowledge"
                     },
                     "confidence": {
                         "type": "number",
                         "minimum": 0,
                         "maximum": 1
                     }
                 },
                 "required": ["name", "primary_domains", "functional_roles", "direct_relationships",
                              "domain_relationships", "confidence"]}



        return {
            "model"          : target_model,
            "response_format": { "type": "json_object" },
            "messages": [ { "role": "system",
                            "content": content_prompt },
                        {   "role": "user",
                            "content": f"Extract key entities from this text: {text}"}],
            "functions": [{
                "name": "extract_entities",
                "description": "Extract entities from text",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entities": {
                            "type": "array",
                            "items": items,
                        }
                    },
                    "required": ["entities"]
                }
            }]
        }

    def create_entity(self, entity_data: Dict[str, Any]) -> Schema__Graph_RAG__Entity:
        entity_node_data = Schema__Graph_RAG__Entity__Data(
            name                 = entity_data['name']                                  ,
            primary_domains      = entity_data['primary_domains']                       ,
            functional_roles     = entity_data['functional_roles']                      ,
            direct_relationships = entity_data['direct_relationships']                  ,
            domain_relationships = entity_data['domain_relationships']                  ,
            ecosystem           = entity_data['ecosystem']                             ,
            confidence          = entity_data.get('confidence', 1.0)                   )

        return Schema__Graph_RAG__Entity(node_data = entity_node_data                  ,
                                         node_id   = Obj_Id()                          ,
                                         node_type = Schema__Graph_RAG__Entity)        # Create entity node from extracted data

    def extract_entities(self, text: str) -> List[Schema__Graph_RAG__Entity]:
        if text in mgraph_llm_cache_simple:
            llm_response = mgraph_llm_cache_simple.get(text)
        else:
            llm_payload     = self.create_entities_prompt(text)                                                 # Generate extraction prompt
            llm_response   = self.api_llm.execute(llm_payload=llm_payload)                                          # Call LLM API

        entities_data  = self.api_llm.get_json__entities(llm_response)                                                # Parse JSON response
        return [self.create_entity(entity) for entity in entities_data]                                     # Convert to typed entities

    def create_relations_prompt(self, entities: List[Schema__Graph_RAG__Entity], text: str) -> str:
        entity_names = [e.node_data.name for e in entities]
        return f"""Analyze the relationships between these entities in the text:
        Entities: {entity_names}
        
        Text: {text}
        
        Return as JSON list of relations with:
        - source: source entity name
        - target: target entity name  
        - relation_type: type of relationship
        - confidence: confidence score (0-1)
        - context: relevant text context"""                                  # Create LLM prompt for relation extraction

    def create_relation(self, relation_data: Dict[str, Any],
                       entities: List[Schema__Graph_RAG__Entity]) -> Schema__Graph_RAG__Relation:
        source = next((e for e in entities
                      if e.node_data.name == relation_data['source']), None)
        target = next((e for e in entities
                      if e.node_data.name == relation_data['target']), None)

        relation_edge_data = Schema__Graph_RAG__Relation__Data( relation_type = relation_data.get('relation_type'  ),
                                                                confidence    = relation_data.get('confidence', 1.0),
                                                                context       = relation_data.get('context'         ),
                                                                attributes    = relation_data.get('attributes', {} ))

        return Schema__Graph_RAG__Relation(
            edge_data=relation_edge_data,
            edge_type=Schema__Graph_RAG__Relation,
            from_node_id=source.node_id,
            to_node_id=target.node_id
        )                                                                    # Create relation from extracted data

    def extract_relations(self, entities: List[Schema__Graph_RAG__Entity],
                         text: str) -> List[Schema__Graph_RAG__Relation]:
        prompt = self.create_relations_prompt(entities, text)                # Generate extraction prompt
        llm_response = self.api_llm.execute(prompt)                         # Call LLM API
        relations_data = self.api_llm.get_json(llm_response)               # Parse JSON response
        return [self.create_relation(relation, entities)
                for relation in relations_data
                if self.valid_relation(relation, entities)]                 # Convert to typed relations

    def valid_relation(self, relation: Dict[str, Any],
                      entities: List[Schema__Graph_RAG__Entity]) -> bool:
        source = next((e for e in entities
                      if e.node_data.name == relation['source']), None)
        target = next((e for e in entities
                      if e.node_data.name == relation['target']), None)
        return source is not None and target is not None                    # Check if relation entities exist


