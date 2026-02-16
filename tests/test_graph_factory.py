import pytest
from src.graph_factory import GraphFactory


class TestGraphFactory:
    @pytest.mark.parametrize("nodes, edges, communities, p_inter", [
        (5, 2, 2, 0.5),
        (10, 4, 3, 0.2),
        (20, 15, 4, 0.1),
        (40, 20, 5, 0.3),
        (65, 34, 6, 0.4),
        (200, 59, 10, 0.5),
        (1000, 563, 20, 0.2),
        (2000, 1000, 50, 0.1),
    ])
    def test_create_graph(self, nodes, edges, communities, p_inter):
        factory = GraphFactory(nodes=nodes, edges=edges, communities=communities, p_inter=p_inter)
        graph, community_graphs = factory.generate_graph()
        assert graph.number_of_nodes() == nodes
        assert graph.number_of_edges() == edges
        assert len(community_graphs) == communities
        for nodo in graph.nodes:
            assert 0 <= graph.nodes[nodo]['opinion'] <= 1
