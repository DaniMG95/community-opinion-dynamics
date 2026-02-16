import networkx as nx
import uuid
import random

class GraphFactory:

    def __init__(self, nodes: int, edges: int, communities: int, p_inter: float):
        if communities > nodes:
            raise ValueError("Number of communities cannot be greater than the number of nodes.")
        if edges > nodes * (nodes - 1) // 2:
            raise ValueError("Number of edges cannot be greater than the maximum possible edges in an undirected graph.")
        self.nodes = nodes
        self.edges = edges
        self.communities = communities
        self.p_inter = p_inter


    def _select_community(self):
        return random.randint(0, self.communities-1)

    def _select_diffs_communities(self):
        community1, community2 = random.sample(range(self.communities), 2)
        return community1, community2

    def _select_type_edge(self):
        return random.random() <= self.p_inter

    def generate_graph(self):
        graph = nx.Graph()
        nodes_per_community = self.nodes // self.communities
        rest_nodes = self.nodes % self.communities
        community_graphs = {}
        for i in range(self.communities):
            community_size = nodes_per_community + (1 if i < rest_nodes else 0)
            nodes = [str(uuid.uuid4()) for _ in range(community_size)]
            rest_nodes -= 1 if i < rest_nodes else 0
            community_graphs[i] = nodes
            graph.add_nodes_from(nodes)

        while graph.number_of_edges() < self.edges:
            if self._select_type_edge():
                community = self._select_community()
                node1, node2 = random.sample(community_graphs[community], 2)
            else:
                community_1, community_2 = self._select_diffs_communities()
                node1 = random.choice(community_graphs[community_1])
                node2 = random.choice(community_graphs[community_2])
            if not graph.has_edge(node1, node2):
                graph.add_edge(node1, node2)

        return graph, community_graphs


