from graph_factory import GraphFactory
from graph_dw import GraphDW

NODES = 1000
EDGES = 5000
COMMUNITIES = 10
D = 0.01
V_CONVERGENCE = 0.25
NUM_EXECUTES = 10
SAVE_RESULTS = True

graph_factory = GraphFactory(NODES, EDGES, COMMUNITIES, 0.3)
graph, communities_nodes = graph_factory.generate_graph()
graph_dw = GraphDW(graph=graph, communities=communities_nodes, d=D,
                   save_history_opinions=SAVE_RESULTS)
graph_dw_clone = graph_dw.clone()
steps = graph_dw.apply_dw(v_convergence=V_CONVERGENCE, confidence_threshold=0.1)
print(steps)
graph_dw.draw_opinions(path=f"opinions_history_0.1_threshold_0.3_p_inter.png")

steps = graph_dw_clone.apply_dw(v_convergence=V_CONVERGENCE, confidence_threshold=0.3, max_steps=steps)
print(steps)
graph_dw_clone.draw_opinions(path=f"opinions_history_0.3_threshold_0.3_p_inter.png")

