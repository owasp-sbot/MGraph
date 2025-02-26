from mgraph_db.providers.graph_rag.mgraph       import MGraph__Graph_RAQ__Entity
from osbot_utils.helpers.Obj_Id                 import Obj_Id
from osbot_utils.type_safe.Type_Safe            import Type_Safe


class Graph_RAG__Create_MGraph(Type_Safe):

    def from_entities(self, entities):
        mgraph_entity = MGraph__Graph_RAQ__Entity()
        with mgraph_entity.builder() as _:
            _.config__unique_values = False
            _.add_node('Text')
            for entity in entities:
                _.root()

                _.add_predicate('entity', entity.name)
                #_.add_predicate('confidence ', entity.confidence).up()

                # adding direct relationships
                _.add_predicate('direct', 'relationships', key=Obj_Id())
                for direct_relationship in entity.direct_relationships:
                   _.add_predicate(direct_relationship.relationship_type, direct_relationship.entity, key=Obj_Id())
                   _.up()
                _.up()

                # adding domain relationships
                _.add_predicate('domain', 'relationships', key=Obj_Id())
                for domain_relationship in entity.domain_relationships:
                    _.add_predicate(domain_relationship.relationship_type, domain_relationship.concept, key=Obj_Id())
                    _.up()
                _.up()
                _.add_predicate('has', 'functional_roles', key=Obj_Id())
                for role in entity.functional_roles:
                    _.add_predicate('role', role).up()
                _.up()

                _.add_predicate('has', 'primary_domains', key=Obj_Id())
                for domain in entity.primary_domains:
                    _.add_predicate('domain', domain).up()
                _.up()
                # adding ecosystem
                if entity.ecosystem.platforms:
                    _.add_predicate('uses', 'platforms', key=Obj_Id())
                    for platform in entity.ecosystem.platforms:
                        _.add_predicate('platform', platform).up()
                    _.up()
                if entity.ecosystem.standards:
                    _.add_predicate('uses', 'standards', key=Obj_Id())
                    for standard in entity.ecosystem.standards:
                        _.add_predicate('standard', standard).up()
                    _.up()
                if entity.ecosystem.technologies:
                    _.add_predicate('uses', 'technologies', key=Obj_Id())
                    for technology in entity.ecosystem.technologies:
                        _.add_predicate('technology', technology).up()
                    _.up()

                _.up()

        return mgraph_entity

    def export_mgraph_to_png(self, mgraph_entity):
        with mgraph_entity.screenshot() as _:
            with _.export().export_dot() as dot:
                dot.set_graph__rank_dir__lr()
                #dot.set_graph__layout_engine__sfdp()
                #dot.set_graph__spring_constant(2)
                #dot.set_graph__overlap__prism1()
                dot.set_node__shape__type__box()
                dot.set_node__shape__rounded()
                dot.show_edge__predicate__str()
                #dot.print_dot_code()

            #_.save_to(f'{self.__class__.__name__}.png')
            _.show_node_value()
            #_.show_edge_type()

            #_.show_node_type()
            png_bytes = _.dot()
            return png_bytes