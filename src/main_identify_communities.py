from graph_factory import GraphFactory
from networkx.algorithms.community.louvain import louvain_communities
import networkx as nx


NODES = 1000
EDGES = 5000
COMMUNITIES = 10
P_INTER = [0.3, 0.9]

for p in P_INTER:
    graph_factory = GraphFactory(NODES, EDGES, COMMUNITIES, p)
    graph, _ = graph_factory.generate_graph()

    communities = louvain_communities(graph)
    for community_id, nodes in enumerate(communities):
        for node in nodes:
            graph.nodes[node]["community"] = community_id

    for node in graph.nodes():
        graph.nodes[node]["label"] = str(node)

    nx.write_gexf(graph, f"grafo_louvain_{p}.gexf")

