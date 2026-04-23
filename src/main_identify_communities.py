from hashlib import algorithms_available

from graph_factory import GraphFactory
from networkx.algorithms.community import (louvain_communities, modularity, k_clique_communities,
                                           greedy_modularity_communities, label_propagation_communities,
                                           leiden_communities, asyn_fluidc)
import networkx as nx

algorithms = {
    "louvain": louvain_communities,
    "k_clique": k_clique_communities,
    "greedy_modularity": greedy_modularity_communities,
    "label_propagation": label_propagation_communities,
    "asyn_fluidc": asyn_fluidc
}

def save_graph_communities(graph, communities, path: str):
    for community_id, nodes in enumerate(communities):
        for node in nodes:
            graph.nodes[node]["community"] = community_id

    for node in graph.nodes():
        graph.nodes[node]["label"] = str(node)

    nx.write_gexf(graph, path)


NODES = 1000
EDGES = 5000
COMMUNITIES = 10
P_INTER = [0.3, 0.9]

graph_factory = GraphFactory(NODES, EDGES, COMMUNITIES, 0.3)
graph_generated, _ = graph_factory.generate_graph()

for i in range(1, 100):
    communities = asyn_fluidc(graph_generated, k=i)
    try:
        mod = modularity(graph_generated, communities)
    except:
        pass
    else:
        print(mod)


# for p in P_INTER:
#     graph_factory = GraphFactory(NODES, EDGES, COMMUNITIES, p)
#     graph_generated, _ = graph_factory.generate_graph()
#
#     for algorithm_name, algorithm_func in algorithms.items():
#
#         if algorithm_name == "asyn_fluidc" or algorithm_name == "k_clique":
#             communities_algorithm = algorithm_func(graph_generated, k=5)
#         else:
#             communities_algorithm = algorithm_func(graph_generated)
#
#         mod = modularity(graph_generated, communities_algorithm)
#         print(f"p_inter: {p} | algorithm {algorithm_name} | Modularity: {mod:.4f}")
