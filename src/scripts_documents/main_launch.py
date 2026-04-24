from community_opinions_dynamics.graph_factory import GraphFactory
from community_opinions_dynamics.graph_dw import GraphDW

NODES = 1000
EDGES = 5000
COMMUNITIES = 10
D = 0.01
V_CONVERGENCE = 0.25
NUM_EXECUTES = 1


for p_inter in [0.3, 0.9]:
    for intent in range(NUM_EXECUTES):
        graph_factory = GraphFactory(NODES, EDGES, COMMUNITIES, p_inter)
        graph, communities_nodes = graph_factory.generate_graph()
        graph_dw = GraphDW(graph=graph, communities=communities_nodes, d=D,
                           save_history_opinions=False)
        graph_dw_clone = graph_dw.clone()
        graph_dw_clone_0_1 = graph_dw.clone()
        graph_dw_clone_0_3 = graph_dw.clone()


        print("Applying DW with confidence threshold 0.1...")
        steps_0_1 = graph_dw.apply_dw(v_convergence=V_CONVERGENCE, confidence_threshold=0.1)
        print(f"Number of steps to convergence: {steps_0_1}")

        print("Applying DW with confidence threshold 0.3...")
        steps_0_3 = graph_dw_clone.apply_dw(v_convergence=V_CONVERGENCE, confidence_threshold=0.3)
        print(f"Number of steps to convergence: {steps_0_3}")

        max_steps = max([steps_0_3, steps_0_1])

        graph_dw_clone_0_1.save_history_opinions = True
        graph_dw_clone_0_3.save_history_opinions = True

        graph_dw_clone_0_1.apply_dw(v_convergence=V_CONVERGENCE, confidence_threshold=0.1, max_steps=max_steps)
        graph_dw_clone_0_1.draw_opinions(path=f"opinions_history_p_inter_{p_inter}_threshold_0_1_{intent}.png",
                                         title=f"Simulation of DW with low ε = 0.1 and Inter. prob.={p_inter}")
        graph_dw_clone_0_3.apply_dw(v_convergence=V_CONVERGENCE, confidence_threshold=0.3, max_steps=max_steps)
        graph_dw_clone_0_3.draw_opinions(path=f"opinions_history_p_inter_{p_inter}_threshold_0_3_{intent}.png",
                                         title=f"Simulation of DW with high ε = 0.3 and Inter. prob.={p_inter}")
