from mgraph_db.providers.simple.MGraph__Simple import MGraph__Simple


class MGraph__Simple__Test_Data(MGraph__Simple):
    test_data : dict

    def create(self):
        with self.edit() as _:
            node_1_id = _.new_node(value='A', name='Node 1').node_id
            node_2_id = _.new_node(value='B', name='Node 2').node_id
            node_3_id = _.new_node(value='C', name='Node 3').node_id
            edge_1_id = _.new_edge(from_node_id=node_1_id, to_node_id=node_2_id).edge_id
            edge_2_id = _.new_edge(from_node_id=node_1_id, to_node_id=node_3_id).edge_id

        self.test_data = {'nodes': [{ 'node_id': node_1_id , 'name'        : 'Node 1'   , 'value'   : 'A'      } ,              # todo: allow this to be customised
                                    { 'node_id': node_2_id , 'name'        : 'Node 2'   , 'value'   : 'B'      } ,
                                    { 'node_id': node_3_id , 'name'        : 'Node 3'   , 'value'   : 'C'      } ],
                          'edges': [{ 'edge_id': edge_1_id  ,'from_node_id': node_1_id, 'to_node_id': node_2_id} ,
                                    { 'edge_id': edge_2_id  ,'from_node_id': node_1_id, 'to_node_id': node_3_id} ]}
        return self

    def edges_ids(self):
        return [edge.get('edge_id') for edge in self.test_data.get('edges')]

    def nodes_ids(self):
        return [node.get('node_id') for node in self.test_data.get('nodes')]


    # def linear_graph(self, num_nodes: int = 3) -> 'MGraph__Static__Graph':                # todo see if something like this is useful                                   # Creates a linear graph where each node connects to the next node in sequence
    #     self.validate_node_count(num_nodes, 1, "linear graph")
    #
    #     with self.graph.edit() as edit:
    #         self.node_ids = self.create_nodes(num_nodes)                                                              # Create nodes
    #         for i in range(num_nodes - 1):                                                                            # Create edges connecting nodes linearly
    #             self.create_edge(self.node_ids[i], self.node_ids[i + 1])
    #     return self