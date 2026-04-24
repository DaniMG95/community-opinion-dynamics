import random

class GraphDW:
    def __init__(self, graph, communities, d, save_history_opinions=True):
        self.graph = graph
        self.communities = communities
        self.d = d
        self.history_opinions = []
        self.save_history_opinions = save_history_opinions

    def clone(self):
        import copy
        return GraphDW(copy.deepcopy(self.graph), copy.deepcopy(self.communities), self.d, self.save_history_opinions)

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

    def apply_dw(self, v_convergence, confidence_threshold, max_steps=0):
        edges = list(self.graph.edges)
        steps = 0
        max_diff = 100000
        if self.save_history_opinions:
            opinions = [self.graph.nodes[node]['opinion'] for node in self.graph.nodes]
            self.history_opinions.append(opinions)
        can_break = False
        while max_diff > self.d or max_steps>steps:
            random.shuffle(edges)
            max_diff = 0
            for random_edge in edges:
                if can_break and steps >= max_steps:
                    max_diff = -1
                    break
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
            if not can_break and max_steps and max_diff < self.d:
                can_break = True
        return steps

    def draw_opinions(self, path: str, title: str):
        import matplotlib
        matplotlib.use('Agg')

        import matplotlib.pyplot as plt
        import numpy as np
        if not self.history_opinions:
            print("No opinions history to plot.")
            return

        plt.figure(figsize=(8, 6), dpi=150)
        sampled_history = np.array(self.history_opinions)[::3000]
        x = np.linspace(0, 1, sampled_history.shape[0])

        plt.scatter(np.zeros(sampled_history.shape[1]), sampled_history[0], color='green', s=8,label="initial opinions")
        for i in range(sampled_history.shape[1]):
            plt.plot(x, sampled_history[:, i], color='blue', alpha=0.03, linewidth=0.5)
        plt.scatter(np.ones(sampled_history.shape[1]), sampled_history[-1], color='red', s=8, label="final opinions")

        plt.scatter([], [], color='blue', s=8, label='updated opinions')

        plt.title(title)
        plt.xlabel("time step")
        plt.ylabel("opinion")
        plt.xlim(-0.02, 1.02)
        plt.ylim(-0.05, 1.05)
        plt.grid()
        plt.legend(loc='lower center', fontsize=8)
        plt.tight_layout()
        plt.savefig(path, bbox_inches='tight', dpi=150)
        plt.close()