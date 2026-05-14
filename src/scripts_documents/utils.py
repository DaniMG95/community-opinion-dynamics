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


def compilate_results(results_path: str, output_file: str):
    from pathlib import Path
    base_path = Path(results_path)
    output_path = Path(output_file)

    with output_path.open("w", encoding="utf-8") as outfile:
        for folder in sorted(base_path.iterdir()):
            if not folder.is_dir():
                continue

            results_file = folder / "results.txt"

            if not results_file.exists():
                continue
            name = folder.name.split("_")
            n = name[1]
            m = name[3]
            k = name[5]
            p = name[7]
            threshold = name[9]
            outfile.write(f"===== N {n} M {m} K {k} P {p} THRESHOLD {threshold} =====\n")

            with results_file.open("r", encoding="utf-8") as infile:
                outfile.write(infile.read())

            outfile.write("\n\n")
