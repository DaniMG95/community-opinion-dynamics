import numpy as np
from numba import njit
from sklearn.cluster import DBSCAN


@njit
def _apply_dw_numba(edges_u, edges_v, opinions, mu, confidence_threshold, d, seed):
    np.random.seed(seed)
    steps = 0
    n_edges = len(edges_u)
    order = np.arange(n_edges)

    max_diff = 100000.0

    while max_diff > d:
        np.random.shuffle(order)
        max_diff = 0.0

        for idx in order:
            u = edges_u[idx]
            v = edges_v[idx]

            opinion_u = opinions[u]
            opinion_v = opinions[v]

            if abs(opinion_u - opinion_v) <= confidence_threshold:
                diff = mu * (opinion_v - opinion_u)

                opinions[u] += diff
                opinions[v] -= diff

                abs_diff = abs(diff)
                if abs_diff > max_diff:
                    max_diff = abs_diff

            steps += 1

    return steps, opinions


@njit
def _apply_dw_max_steps_numba(edges_u, edges_v, opinions, mu, confidence_threshold, max_steps):
    steps = 0
    n_edges = len(edges_u)

    order = np.arange(n_edges)

    while steps < max_steps:
        np.random.shuffle(order)

        for idx in order:
            if steps >= max_steps:
                break

            u = edges_u[idx]
            v = edges_v[idx]

            opinion_u = opinions[u]
            opinion_v = opinions[v]

            if abs(opinion_u - opinion_v) < confidence_threshold:
                diff = mu * (opinion_v - opinion_u)
                opinions[u] += diff
                opinions[v] -= diff

            steps += 1

    return steps, opinions


class GraphDWOptimized:
    def __init__(self, graph, communities, d, save_history_opinions=False):
        self.graph = graph
        self.communities = communities
        self.d = d
        self.save_history_opinions = save_history_opinions
        self.history_opinions = []
        self.last_steps = None

        self.node_to_idx = {
            node: idx
            for idx, node in enumerate(self.graph.nodes)
        }

        self.idx_to_node = {
            idx: node
            for node, idx in self.node_to_idx.items()
        }

        self.edges_u, self.edges_v = self._build_edges_arrays()
        self.opinions = self._build_opinions_array()

    def _build_edges_arrays(self):
        edges_u = []
        edges_v = []

        for u, v in self.graph.edges:
            edges_u.append(self.node_to_idx[u])
            edges_v.append(self.node_to_idx[v])

        return (
            np.array(edges_u, dtype=np.int64),
            np.array(edges_v, dtype=np.int64)
        )

    def _build_opinions_array(self):
        opinions = np.zeros(len(self.node_to_idx), dtype=np.float64)

        for node, idx in self.node_to_idx.items():
            opinions[idx] = self.graph.nodes[node]["opinion"]

        return opinions

    def _sync_opinions_to_graph(self):
        for idx, opinion in enumerate(self.opinions):
            node = self.idx_to_node[idx]
            self.graph.nodes[node]["opinion"] = float(opinion)

    def clone(self):
        import copy
        return GraphDWOptimized(
            copy.deepcopy(self.graph),
            copy.deepcopy(self.communities),
            self.d,
            self.save_history_opinions
        )

    def apply_dw(self, v_convergence, confidence_threshold, seed):
        if self.save_history_opinions:
            self.history_opinions.append(self.opinions.copy())

        steps, final_opinions = _apply_dw_numba(
            self.edges_u,
            self.edges_v,
            self.opinions.copy(),
            v_convergence,
            confidence_threshold,
            self.d, seed=seed
        )

        self.opinions = final_opinions
        self.last_steps = steps
        self._sync_opinions_to_graph()

        if self.save_history_opinions:
            self.history_opinions.append(self.opinions.copy())

        return steps

    def apply_dw_max_steps(self, v_convergence, confidence_threshold, max_steps):
        if self.save_history_opinions:
            self.history_opinions.append(self.opinions.copy())

        steps, final_opinions = _apply_dw_max_steps_numba(
            self.edges_u,
            self.edges_v,
            self.opinions.copy(),
            v_convergence,
            confidence_threshold,
            max_steps
        )

        self.opinions = final_opinions
        self.last_steps = steps
        self._sync_opinions_to_graph()

        if self.save_history_opinions:
            self.history_opinions.append(self.opinions.copy())

        return steps

    def get_final_opinions(self):
        return self.opinions.copy()

    def count_opinion_clusters_dbscan(self, eps=0.01, min_samples_ratio=0.01):
        final_opinions = np.array(self.get_final_opinions()).reshape(-1, 1)

        min_samples = max(3, int(len(final_opinions) * min_samples_ratio))

        labels = DBSCAN(
            eps=eps,
            min_samples=min_samples,
        ).fit_predict(final_opinions)

        cluster_labels = set(labels)
        cluster_labels.discard(-1)

        return len(cluster_labels)

    def has_consensus(self):
        return self.count_opinion_clusters_dbscan() == 1

    def get_sweeps(self, steps):
        return steps / len(self.edges_u)

    def draw_graph(self):
        import matplotlib.pyplot as plt
        import networkx as nx
        import matplotlib.cm as cm

        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(self.graph, k=0.5, iterations=50)

        n_communities = len(self.communities)
        colours = cm.rainbow(np.linspace(0, 1, n_communities))

        nx.draw_networkx_edges(self.graph, pos, alpha=0.3, edge_color="gray")

        for (label_community, nodes_community), colour in zip(self.communities.items(), colours):
            nx.draw_networkx_nodes(
                self.graph,
                pos,
                nodelist=nodes_community,
                node_color=[colour],
                label=label_community,
                node_size=300
            )

        plt.title("Graph")
        plt.legend(scatterpoints=1)
        plt.axis("off")
        plt.show()

    def draw_opinions(self, path: str, title: str):
        import matplotlib
        matplotlib.use("Agg")

        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle
        import numpy as np

        if not self.history_opinions:
            print("No opinions history to plot.")
            return

        history = np.array(self.history_opinions)
        step = 4000

        total_steps = self.last_steps if self.last_steps is not None else len(history) - 1
        history_steps = np.linspace(0, total_steps, len(history))

        sampled_history = history[::step]
        x = history_steps[::step]

        if x[-1] != total_steps:
            sampled_history = np.vstack([sampled_history, history[-1]])
            x = np.append(x, total_steps)

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
        ax.set_xlim(0, total_steps)
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
                color = "red"

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
        fig.add_artist(
            Rectangle(
                (0.01, 0.01),
                0.98,
                0.98,
                transform=fig.transFigure,
                fill=False,
                edgecolor="black",
                linewidth=1.2,
                clip_on=False,
                zorder=10
            )
        )

        plt.savefig(path, bbox_inches="tight", dpi=150)
        plt.close()
