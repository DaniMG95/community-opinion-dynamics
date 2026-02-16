class GraphDW:
    def __init__(self, graph, communities):
        self.graph = graph
        self.communities = communities

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