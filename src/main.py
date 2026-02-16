from graph_factory import GraphFactory
from graph import GraphDW

graph_factory = GraphFactory(nodes=1000, edges=5000, communities=10, p_inter=0.7)

graph, communities_nodes = graph_factory.generate_graph()

graph_dw = GraphDW(graph=graph, communities=communities_nodes, d=0.00001)
steps = graph_dw.apply_dw(v_convergence=0.25, confidence_threshold=0.3)
print(f"Number of steps to convergence: {steps}")
graph_dw.draw_opinions(path="opinions_history.png")