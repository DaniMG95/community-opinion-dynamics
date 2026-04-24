import networkx as nx
from networkx.algorithms.community import modularity, k_clique_communities, asyn_fluidc

def draw_graph(x: list, y: list, title: str, xlabel: str, ylabel: str, path: str) -> None:
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 6), dpi=150)
    plt.plot(x, y, marker='o')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.savefig(path, bbox_inches='tight', dpi=150)
    plt.close()

def save_graph_communities(graph, communities, path: str):
    for community_id, nodes in enumerate(communities):
        for node in nodes:
            graph.nodes[node]["community"] = community_id

    for node in graph.nodes():
        graph.nodes[node]["label"] = str(node)

    nx.write_gexf(graph, path)

def overlapping_to_partition(G, communities):
    assigned = set()
    partition = []

    for comm in communities:
        clean_comm = set(comm) - assigned
        if clean_comm:
            partition.append(clean_comm)
            assigned.update(clean_comm)

    for node in G.nodes():
        if node not in assigned:
            partition.append({node})

    return partition

def compute_modularity_k_clique(graph):
    max_mod = 0
    max_k = 0
    for i in [3, 4, 5]:
        communities = k_clique_communities(graph, k=i)
        try:
            communities = list(communities)
            partition = overlapping_to_partition(graph, communities)
            mod = modularity(graph, partition)
        except:
            pass
        else:
            if mod > max_mod:
                max_mod = mod
                max_k = i
    return max_k, max_mod

def compute_modularity_asyn_fluidc(graph):
    max_mod = 0
    max_k = 0
    for i in range(2, 11):
        try:
            communities = asyn_fluidc(graph, k=i)
            mod = modularity(graph, communities)
        except:
            pass
        else:
            if mod > max_mod:
                max_mod = mod
                max_k = i
    return max_k, max_mod