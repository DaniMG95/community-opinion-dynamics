from graph_factory import GraphFactory
from graph import GraphDW


graph_factory = GraphFactory(nodes=20, edges=40, communities=3, p_inter=0.7)

graph, communities_nodes = graph_factory.generate_graph()

graph_dw = GraphDW(graph, communities_nodes)
graph_dw.draw_graph()
