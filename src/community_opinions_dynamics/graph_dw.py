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

        history = np.array(self.history_opinions)
        step = 4000

        sampled_history = history[::step]
        x = np.arange(0, len(history), step)

        if x[-1] != len(history) - 1:
            sampled_history = np.vstack([sampled_history, history[-1]])
            x = np.append(x, len(history) - 1)

        n_agents = sampled_history.shape[1]

        fig, (ax, ax_hist) = plt.subplots(
            1, 2,
            figsize=(8.5, 6),
            dpi=150,
            sharey=True,
            gridspec_kw={
                "width_ratios": [28, 1.4],
                "wspace": 0.03
            }
        )

        ax.scatter(
            np.zeros(n_agents),
            sampled_history[0],
            color='green',
            s=8,
            label='initial opinions',
            zorder=3
        )

        for i in range(n_agents):
            ax.plot(
                x,
                sampled_history[:, i],
                color='blue',
                alpha=0.03,
                linewidth=0.5
            )

        ax.scatter(
            np.full(n_agents, x[-1]),
            sampled_history[-1],
            color='red',
            s=8,
            label='final opinions',
            zorder=3
        )

        ax.scatter([], [], color='blue', s=8, label='updated opinions')

        ax.set_title(title)
        ax.set_xlabel("time step")
        ax.set_ylabel("opinion")
        ax.set_ylim(0, 1)
        ax.grid(alpha=0.6)
        ax.legend(loc="lower center", fontsize=8)

        final_opinions = history[-1]

        counts, bins = np.histogram(
            final_opinions,
            bins=40,
            range=(0, 1)
        )

        bin_centers = (bins[:-1] + bins[1:]) / 2

        ax_hist.set_xlim(0, 1.05)
        ax_hist.set_xticks([])
        ax_hist.grid(False)
        ax_hist.set_ylim(0, 1)

        ax_hist.spines["left"].set_visible(False)
        ax_hist.spines["top"].set_visible(False)
        ax_hist.spines["bottom"].set_visible(False)
        ax_hist.spines["right"].set_visible(False)

        max_count = counts.max() if counts.max() > 0 else 1

        freq_threshold = 0.8

        for c, y in zip(counts, bin_centers):
            if c > 0:
                relative_freq = c / max_count
                color = "red" if relative_freq > freq_threshold else "green"

                ax_hist.hlines(
                    y=y,
                    xmin=0,
                    xmax=relative_freq,
                    color=color,
                    linewidth=2.5,
                    alpha=0.9
                )

        yticks = np.linspace(0, 1, 6)
        ax_hist.set_yticks(yticks)
        ax_hist.set_yticklabels([f"{v:.1f}" for v in yticks])

        ax_hist.yaxis.tick_right()
        ax_hist.yaxis.set_label_position("right")
        ax_hist.tick_params(
            axis='y',
            right=True,
            labelright=True,
            left=False,
            labelleft=False,
            labelsize=8
        )

        ax_hist_top = ax_hist.secondary_xaxis('top')
        ax_hist_top.set_xticks([0.01, 1.0])
        ax_hist_top.set_xticklabels(['1%', '100%'])
        ax_hist_top.tick_params(axis='x', labelsize=7, pad=2, length=0)

        fig.text(
            0.995, 0.5,
            "final distribution",
            rotation=90,
            ha="center",
            va="center",
            fontsize=9,
            color="black"
        )

        plt.subplots_adjust(right=0.95)

        plt.savefig(path, bbox_inches="tight", dpi=150)
        plt.close()