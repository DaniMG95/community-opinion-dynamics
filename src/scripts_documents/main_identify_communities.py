from community_opinions_dynamics.graph_factory import GraphFactory
from networkx.algorithms.community import (louvain_communities, modularity,
                                           greedy_modularity_communities, label_propagation_communities)
from utils import compute_modularity_asyn_fluidc
import statistics


algorithms = {
    "louvain": louvain_communities,
    "greedy_modularity": greedy_modularity_communities,
    "label_propagation": label_propagation_communities,
}



NODES = 1000
EDGES = 5000
N_SIMULATORS = 100
STEPS = 10
COMMUNITIES = 10
P_INTER = [0.3, 0.5, 0.7, 0.9]


for p in P_INTER:
    history_modularity = {algorithm: [] for algorithm in algorithms.keys()}
    history_modularity["asyn_fluidc"] = []
    k_values_clique = set()
    k_values_fluidc = set()

    for i in range(N_SIMULATORS):
        print("Step:", i, "p_inter:", p)
        graph_factory = GraphFactory(NODES, EDGES, COMMUNITIES, p)
        graph_generated, _ = graph_factory.generate_graph()

        k, mod = compute_modularity_asyn_fluidc(graph=graph_generated)
        history_modularity["asyn_fluidc"].append(mod)
        k_values_fluidc.add(k)

        for algorithm_name, algorithm_func in algorithms.items():
            communities_algorithm = algorithm_func(graph_generated)
            mod = modularity(graph_generated, communities_algorithm)
            history_modularity[algorithm_name].append(mod)

    for algorithm_name in history_modularity.keys():
        if algorithm_name == "k_clique":
            print(f"k values: {k_values_clique}")
        elif algorithm_name == "asyn_fluidc":
            print(f"k values: {k_values_fluidc}")
        mean_modularity_alg = statistics.mean(history_modularity[algorithm_name])
        std_alg = statistics.stdev(history_modularity[algorithm_name])
        print(f"p_inter={p:.2f}, Algorithm: {algorithm_name}, Mean Modularity: {mean_modularity_alg:.4f}, "
              f"Std Dev: {std_alg:.4f}")
