import random

class GraphDW:
    def __init__(self, graph, communities, d, save_history_opinions=True):
        self.graph = graph
        self.communities = communities
        self.d = d
        self.history_opinions = []
        self.save_history_opinions = save_history_opinions

    def draw_graph(self):
        import matplotlib.pyplot as plt
        import networkx as nx
        import matplotlib.cm as cm
        import numpy as np

        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(self.graph, k=0.5, iterations=50)

        n_communities = len(self.communities)
        colours = cm.rainbow(np.linspace(0, 1, n_communities))
        nx.draw_networkx_edges(self.graph, pos, alpha=0.3, edge_color='gray')
        for (label_community, nodes_community), colour in zip(self.communities.items(), colours):
            nx.draw_networkx_nodes(
                self.graph,
                pos,
                nodelist=nodes_community,
                node_color=colour,
                label=label_community,
                node_size=300
            )

        plt.title("Graph")
        plt.legend(scatterpoints=1)
        plt.axis('off')
        plt.show()

    def apply_dw(self, v_convergence, confidence_threshold, max_steps = 0):
        edges = list(self.graph.edges)
        steps = 0
        max_diff = 100000
        if self.save_history_opinions:
            opinions = [self.graph.nodes[node]['opinion'] for node in self.graph.nodes]
            self.history_opinions.append(opinions)
        while max_diff > self.d and steps <= max_steps:
            random.shuffle(edges)
            max_diff = 0
            for random_edge in edges:
                node1, node2 = random_edge
                opinion1 = self.graph.nodes[node1]['opinion']
                opinion2 = self.graph.nodes[node2]['opinion']
                if abs(opinion1 - opinion2) <= confidence_threshold:
                    diff = v_convergence * (opinion2 - opinion1)
                    self.graph.nodes[node1]['opinion'] += diff
                    self.graph.nodes[node2]['opinion'] -= diff
                    if abs(diff) > max_diff:
                        max_diff = abs(diff)
                steps += 1
                if self.save_history_opinions:
                    opinions = [self.graph.nodes[node]['opinion'] for node in self.graph.nodes]
                    self.history_opinions.append(opinions)
        return steps

    def draw_opinions(self, path: str):
        import matplotlib
        matplotlib.use('Agg')

        import matplotlib.pyplot as plt
        import numpy as np
        if not self.history_opinions:
            print("No opinions history to plot.")
            return

        history_opinions = np.array(self.history_opinions)
        plt.figure(figsize=(20, 12), dpi=150)
        for i in range(history_opinions.shape[1]):
            plt.plot(history_opinions[::1000, i], color='steelblue', linestyle='-', alpha=0.05, lw=0.5)
        plt.title("Evolution of Opinions - Large Scale Simulation", fontsize=20)
        plt.xlabel("Simulation Steps", fontsize=15)
        plt.ylabel("Opinion Value", fontsize=15)
        plt.ylim(-0.05, 1.05)
        plt.grid(True, which='both', linestyle='--', alpha=0.2)
        plt.savefig(path, bbox_inches='tight', dpi=150)
        plt.close()